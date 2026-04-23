from flask import Flask, render_template, request, jsonify, session, send_from_directory
import os
from datetime import datetime
from src.config import client_agent, AGENT_SYSTEM_PROMPT, NR_HISTORY
from src.retrieval import process_query, rerank_query

app = Flask(__name__)
app.secret_key = os.urandom(24)

conversation_store: dict[str, list] = {}
turn_counter: dict[str, int] = {}
conversation_start: dict[str, str] = {}

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
    log_path = os.path.join(LOGS_DIR, f"output_{conversation_start[session_id]}.txt")
    is_new = not os.path.exists(log_path)
    with open(log_path, "a", encoding="utf-8") as f:
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
            page = metadata.get("page_start", 0) + 1
            f.write(f"  Rank {rank} | distance={distance:.6f} | page={page}\n")
            f.write(f"  Metadata : {metadata}\n")
            f.write(f"  Content  : {content}\n\n")
        f.write("GENERATED RESPONSE\n")
        f.write(response + "\n")
        f.write("\n")


def get_messages(session_id: str) -> list:
    if session_id not in conversation_store:
        conversation_store[session_id] = [
            {"role": "system", "content": AGENT_SYSTEM_PROMPT}
        ]
    return conversation_store[session_id]


@app.route("/")
def index():
    if "session_id" not in session:
        session["session_id"] = os.urandom(16).hex()
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)
    if not data or not data.get("message", "").strip():
        return jsonify({"error": "Empty message"}), 400

    query = data["message"].strip()
    session_id = session.get("session_id", "default")
    messages = get_messages(session_id)

    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if session_id not in conversation_start:
            conversation_start[session_id] = datetime.now().strftime("%Y%m%d_%H%M%S")
        results = process_query(query)
        reranked_results = rerank_query(query, results)
        #TODO: build security features to prevent prompt injection attacks since the retrieved chunks are directly included in the prompt
        # also to prevent queries that are not related to the document and just try to manipulate the model into giving wrong answers
        top = reranked_results[0] if reranked_results else ("No relevant information found.", {}, 0.0)
        content, metadata = top[0], top[1]
        page = metadata.get("page_start", 0) + 1
        metadata_with_page = {**metadata, "page_start": page}

        messages.append({
            "role": "user",
            "content": (
                f"Query of the user: {query}. "
                f"Retrieved text from the document: {content}. "
                f"Source: {metadata_with_page}"
            ),
        })

        completion = client_agent.chat.completions.create(
            messages=[messages[0]] + messages[-NR_HISTORY:],
            model="llama-3.3-70b-versatile",
        )
        response = completion.choices[0].message.content
        messages.append({"role": "assistant", "content": response})

        turn_counter[session_id] = turn_counter.get(session_id, 0) + 1
        write_conversation_log(
            session_id=session_id,
            timestamp=timestamp,
            query=query,
            retrieval_results=results if results else [],
            system_prompt=AGENT_SYSTEM_PROMPT,
            response=response,
            turn=turn_counter[session_id],
        )

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/conversations", methods=["GET"])
def list_conversations():
    convs = []
    for fname in sorted(os.listdir(LOGS_DIR), reverse=True):
        if not fname.startswith("output_") or not fname.endswith(".txt"):
            continue
        name = fname[len("output_"):-len(".txt")]  # YYYYMMDD_HHMMSS
        try:
            dt = datetime.strptime(name, "%Y%m%d_%H%M%S")
            started = dt.strftime("%b %d, %Y %H:%M")
        except ValueError:
            started = name
        convs.append({
            "filename": fname,
            "started": started,
        })
    return jsonify(convs)


@app.route("/conversations/<filename>", methods=["GET"])
def download_conversation(filename):
    safe_name = os.path.basename(filename)
    if not safe_name.startswith("output_") or not safe_name.endswith(".txt"):
        return jsonify({"error": "Invalid filename"}), 400
    return send_from_directory(LOGS_DIR, safe_name, mimetype="text/plain")


@app.route("/reset", methods=["POST"])
def reset():
    session_id = session.get("session_id", "default")
    if session_id in conversation_store:
        del conversation_store[session_id]
    turn_counter.pop(session_id, None)
    conversation_start.pop(session_id, None)
    session["session_id"] = os.urandom(16).hex()
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
