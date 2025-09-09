from tensorzero import TensorZeroGateway, ToolCall
from retriever import build_chunks, get_relevant_chunks
import json

# --- Step 1: Load question from input.json ---
with open("sources/input.json", "r", encoding="utf-8") as f:
    input_data = json.load(f)
    question = input_data["content"]

# --- Step 2: Build source chunks ---
all_chunks = build_chunks()

with open("sample.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    content = data["content"]

with TensorZeroGateway.build_embedded(
    clickhouse_url="http://chuser:chpassword@localhost:8123/tensorzero",
    config_file="config/tensorzero.toml",
) as client:

    relevant_chunks = get_relevant_chunks(question, all_chunks)

# Build sources according to schema
sources = [
    {
        "type": "text",
        "contents": chunk
    }
    for chunk in relevant_chunks
]

# Build input object following your schema
input_obj = {
    "input": question,
    "sources": sources
}

# Send inference request
response = client.inference(
    function_name="synthesise_content",
    input={
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "arguments": input_obj
                    }
                ]
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
            metric_name="user_rating",
            episode_id=response.episode_id,
            value=float(rating),
        )
        print("Feedback recorded:", feedback_result)

        
else:
    print("Invalid input. Please enter a number between 1 and 5.")