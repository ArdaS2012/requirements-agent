from .config import client_agent, AGENT_SYSTEM_PROMPT
from .retrieval import process_query


def start_agent():
    print("Agent started. Listening for tasks...")
    messages = [
        {
            "role": "system",
            "content": AGENT_SYSTEM_PROMPT,
        }
    ]
    while True:
        query = input("Ask me something about the requirements or type 'exit' to stop: ")
        if query.lower() == "exit":
            print("Agent stopped.")
            break

        processed_query = process_query(query)
        #TODO: rerank the retrieved chunks and select the most relevant ones to include in the prompt
        #For now only take the most relevant chunk
        processed_query = [processed_query[0]] if processed_query else [("No relevant information found in the document.", {})]
        content, metadata = processed_query[0][0], processed_query[0][1]
        metadata["page_start"] = metadata["page_start"] + 1 #Since the page numbers start from 1 and not 0
        messages.append({
            "role": "user",
            "content": f"Query of the user:{query}. Retrieved text from the document: {content}. Source: {metadata}",
        })
        chat_completion = client_agent.chat.completions.create(
            messages=[messages[0]] + messages[-4:],
            model="llama-3.3-70b-versatile",
        )
        response = chat_completion.choices[0].message.content
        messages.append({
            "role": "assistant",
            "content": response,
        })
        print(f"ReqBot: {response}")
        
    print("Agent has been stopped.")
    print("Have a good day!")