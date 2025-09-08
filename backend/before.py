import os
from openai import OpenAI

# Set your OpenAI API key as an environment variable
# You can get your API key from: https://platform.openai.com/api-keys
# Set it by running: export OPENAI_API_KEY="your-api-key-here"

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "Write a haiku about artificial intelligence.",
        }
    ],
)

print(response)