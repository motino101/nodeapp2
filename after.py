from tensorzero import TensorZeroGateway
import json
# Example: take an input field (content) and a guidin
# g question

with open("sample.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    content = data["content"]

with TensorZeroGateway.build_embedded(
    clickhouse_url="http://chuser:chpassword@localhost:8123/tensorzero",
    config_file="config/tensorzero.toml",
) as client:
    response = client.inference(
        function_name="synthesise_content",
        input={
            "messages": [
                {
                    "role": "user",
                    "content": f"Please draft a piece of content using the following information:\n\n- Source content: {content}\n- Task: Synthesise my sources into a 1-minute video script."
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