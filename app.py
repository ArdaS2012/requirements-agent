from flask import Flask, render_template, request, jsonify, session, send_from_directory
import os
from datetime import datetime
from src.config import client_agent, AGENT_SYSTEM_PROMPT, NR_HISTORY, llm_pipeline
from src.retrieval import process_query, rerank_query

app = Flask(__name__)
# Secret key for signing Flask session cookies; regenerated on every restart
app.secret_key = os.urandom(24)

# In-memory stores keyed by session_id (browser-session scoped):
conversation_store: dict[str, list] = {}   # full message history per session
turn_counter: dict[str, int] = {}          # number of turns taken per session
conversation_start: dict[str, str] = {}    # timestamp of session start (for log filenames)

# Directory where per-session conversation logs are persisted as plain-text files
LOGS_DIR = os.path.join(os.path.dirname(__file__), "outputs", "logs")
os.makedirs(LOGS_DIR, exist_ok=True)


def write_conversation_log(
    session_id: str,
    timestamp: str,
    query: str,
    retrieval_results: list,
    system_prompt: str,
    response: str,
    turn: int,
) -> None:
    """Append a single turn's details to the session's log file.

    The log file is created on the first turn and appended to on every
    subsequent turn, so the full conversation can be reviewed offline.
    Each turn records the user query, the top-3 retrieved chunks with their
    distances, and the final LLM response.

    Args:
        session_id:        Unique identifier for the browser session.
        timestamp:         Human-readable datetime string for this turn.
        query:             The raw user message.
        retrieval_results: Rows returned by process_query() (before reranking).
        system_prompt:     The system prompt sent to the LLM this turn.
        response:          The LLM's answer after output validation.
        turn:              Sequential turn number within the session.
    """
    log_path = os.path.join(LOGS_DIR, f"output_{conversation_start[session_id]}.txt")
    is_new = not os.path.exists(log_path)
    with open(log_path, "a", encoding="utf-8") as f:
        # Write a one-time header block at the start of a new log file
        if is_new:
            f.write("=" * 80 + "\n")
            f.write(f"Conversation ID : {session_id}\n")
            f.write(f"Started         : {timestamp}\n")
            f.write("-" * 80 + "\n")
            f.write("SYSTEM PROMPT\n")
            f.write(system_prompt + "\n")
            f.write("=" * 80 + "\n\n")

        f.write(f"--- Turn {turn} | {timestamp} " + "-" * (54 - len(str(turn))) + "\n")
        f.write(f"USER QUERY\n{query}\n\n")
        f.write("TOP 3 RETRIEVED CHUNKS\n")
        for rank, row in enumerate(retrieval_results[:3], start=1):
            content, metadata, distance = row[0], row[1], row[2]
            page = metadata.get("page_start", 0) + 1  # convert 0-based to 1-based
            f.write(f"  Rank {rank} | distance={distance:.6f} | page={page}\n")
            f.write(f"  Metadata : {metadata}\n")
            f.write(f"  Content  : {content}\n\n")
        f.write("GENERATED RESPONSE\n")
        f.write(response + "\n")
        f.write("\n")


def get_messages(session_id: str) -> list:
    """Return (or initialise) the conversation history for a session.

    The history is stored in conversation_store in memory.  The system prompt
    is always prepended as the first message so that new sessions start
    with the correct LLM persona.
    """
    if session_id not in conversation_store:
        conversation_store[session_id] = [
            {"role": "system", "content": AGENT_SYSTEM_PROMPT}
        ]
    return conversation_store[session_id]


@app.route("/")
def index():
    # Assign a random session ID if this is a new browser session
    if "session_id" not in session:
        session["session_id"] = os.urandom(16).hex()
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """Handle a single chat turn.

    Flow:
    1. Parse and validate the JSON payload.
    2. Run vector search + cross-encoder reranking.
    3. Pass the top result and user query through SecureLLMPipeline.
    4. Log the full turn and return the response as JSON.
    """
    data = request.get_json(silent=True)
    if not data or not data.get("message", "").strip():
        return jsonify({"error": "Empty message"}), 400

    query = data["message"].strip()
    session_id = session.get("session_id", "default")

    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Record session start timestamp so the log filename stays stable
        if session_id not in conversation_start:
            conversation_start[session_id] = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Step 1: vector search returns top-5 candidates (content, metadata, distance)
        results = process_query(query)

        # Step 2: cross-encoder reranking for precision — pick the single best chunk
        reranked_results = rerank_query(query, results)
        top = reranked_results[0] if reranked_results else ("No relevant information found.", {}, 0.0)
        content, metadata = top[0], top[1]
        page = metadata.get("page_start", 0) + 1  # convert 0-based to 1-based page number
        metadata_with_page = {**metadata, "page_start": page}

        # Step 3: build a security-hardened system prompt and call the LLM pipeline
        system_prompt = llm_pipeline.generate_system_prompt(
            "Requirement Analyst",
            "Answering user queries about requirement documents based on retrieved information.",
        )
        response = llm_pipeline.process_request(query, system_prompt, content)

        # Step 4: log the turn and increment the turn counter
        turn_counter[session_id] = turn_counter.get(session_id, 0) + 1
        write_conversation_log(
            session_id=session_id,
            timestamp=timestamp,
            query=query,
            retrieval_results=results if results else [],
            system_prompt=system_prompt,
            response=response,
            turn=turn_counter[session_id],
        )

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/conversations", methods=["GET"])
def list_conversations():
    """Return a JSON list of all saved conversation log files, newest first."""
    convs = []
    for fname in sorted(os.listdir(LOGS_DIR), reverse=True):
        if not fname.startswith("output_") or not fname.endswith(".txt"):
            continue
        name = fname[len("output_"):-len(".txt")]  # extract YYYYMMDD_HHMMSS portion
        try:
            dt = datetime.strptime(name, "%Y%m%d_%H%M%S")
            started = dt.strftime("%b %d, %Y %H:%M")
        except ValueError:
            started = name  # fall back to raw string if format doesn't match
        convs.append({
            "filename": fname,
            "started": started,
        })
    return jsonify(convs)


@app.route("/conversations/<filename>", methods=["GET"])
def download_conversation(filename):
    """Serve a conversation log file for download or in-browser viewing.

    The filename is validated against the expected naming convention to
    prevent directory traversal attacks.
    """
    safe_name = os.path.basename(filename)  # strip any path components
    if not safe_name.startswith("output_") or not safe_name.endswith(".txt"):
        return jsonify({"error": "Invalid filename"}), 400
    return send_from_directory(LOGS_DIR, safe_name, mimetype="text/plain")


@app.route("/reset", methods=["POST"])
def reset():
    """Clear the current session's conversation history and start a fresh one.

    This deletes the in-memory message list and assigns a new random session
    ID so the next request begins with a clean slate.
    """
    session_id = session.get("session_id", "default")
    if session_id in conversation_store:
        del conversation_store[session_id]
    llm_pipeline.messages = []  # also reset the pipeline's internal history
    turn_counter.pop(session_id, None)
    conversation_start.pop(session_id, None)
    session["session_id"] = os.urandom(16).hex()
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
