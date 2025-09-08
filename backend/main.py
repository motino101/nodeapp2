from tensorzero import TensorZeroGateway, ToolCall
from retriever import build_chunks, get_relevant_chunks
import json

# --- Step 1: User provides a question ---
question = "Synthesise my sources into a 1-minute video script about farming and climate change."

# --- Step 2: Build source chunks ---
all_chunks = build_chunks()


with open("sample.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    content = data["content"]

with TensorZeroGateway.build_embedded(
    clickhouse_url="http://chuser:chpassword@localhost:8123/tensorzero",
    config_file="config/tensorzero.toml",
) as client:

    # run first function - reformulate question into search query
    query_resp = client.inference(
        function_name="generate_research_query",
        input={
            "messages": [
                {
                    "role": "user",
                    "content": f"Question: {question}",
                }
            ]
        }
    )
    print(query_resp)
    search_query = query_resp

    # run second function - synthesise content
    relevant_chunks = get_relevant_chunks(search_query, all_chunks)

    response = client.inference(
        function_name="synthesise_content",
        episode_id=query_resp.episode_id, # use episode id to link the two inferences
        input={
            "messages": [
                {
                    "role": "user",
                    "content": f"Question: {question}\nSources: {relevant_chunks}",
                }
            ]
        },
    )

print(response)


# --- FEEDBACK SECTION --
feedback = input("How useful was this? (1-5): ").strip().lower()

if feedback.isdigit() and 1 <= int(feedback) <= 5:
    rating = int(feedback)
    
    # Use HTTP client for feedback
    with TensorZeroGateway.build_http(gateway_url="http://localhost:3000") as feedback_client:
        feedback_result = feedback_client.feedback(
            metric_name="synthesis_quality",
            inference_id=response.inference_id,
            value=float(rating),
        )
        print("Feedback recorded:", feedback_result)
else:
    print("Invalid input. Please enter a number between 1 and 5.")