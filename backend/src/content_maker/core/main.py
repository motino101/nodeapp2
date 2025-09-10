from tensorzero import TensorZeroGateway, ToolCall
from .retriever import build_chunks, get_relevant_chunks
from ..processors.source_detector import SmartSourceDetector
import json
import os
import time

def main():
    """Main function for Content Maker"""
    # --- Step 1: Load question from input.json ---
    with open("sources/input.json", "r", encoding="utf-8") as f:
        input_data = json.load(f)
        question = input_data["content"]

    # --- Step 2: Build source chunks ---
    all_chunks = build_chunks()

    with TensorZeroGateway.build_embedded(
        clickhouse_url="http://chuser:chpassword@localhost:8123/tensorzero",
        config_file="config/tensorzero.toml",
    ) as client:

        relevant_chunks = get_relevant_chunks(question, all_chunks)

    # --- SMART SOURCE DETECTION AND PROCESSING ---
    # Smart source detection and processing
    detector = SmartSourceDetector()
    all_sources = detector.process_sources_directory("sources")

    # Build sources according to schema (combine with relevant chunks)
    sources = [
        {
            "type": "text",
            "contents": chunk
        }
        for chunk in relevant_chunks
    ]

    # Add processed sources from smart detection
    sources.extend(all_sources)

    # Clean up sources to match the threading schema (remove extra properties)
    cleaned_sources = []
    for source in sources:
        cleaned_source = {
            "type": source["type"],
            "contents": source["contents"]
        }
        cleaned_sources.append(cleaned_source)

    print(f"Processing {len(cleaned_sources)} sources...")

    # --- NEW STEP 1: Thread Ideas ---
    print("Step 1: Threading ideas from sources...")
    threading_input = {
        "input": question,
        "sources": cleaned_sources
    }

    threading_response = client.inference(
        function_name="thread_ideas",
        input={
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "arguments": threading_input
                        }
                    ]
                }
            ]
        },
    )

    print("Threading complete. Found threads:")
    threads_data = threading_response.output.parsed

    if threads_data is None:
        print("Error: No threads data received. Falling back to original sources only.")
        # Fallback to original sources
        synthesis_input = {
            "input": question,
            "sources": cleaned_sources,
            "threads": [],
            "thread_summary": "No threads available - using original sources only",
            "additional_instructions": ""
        }
    else:
        for i, thread in enumerate(threads_data["threads"], 1):
            print(f"{i}. {thread['title']}")
            print(f"   {thread['insight']}")
            print()

        # --- USER SELECTION STEP ---
        print("Which thread would you like to focus on for the video script?")
        print("Enter the number (1-{}) or 'all' to use all threads:".format(len(threads_data["threads"])))
        choice = input("Your choice: ").strip()

        selected_threads = []
        if choice.lower() == 'all':
            selected_threads = threads_data["threads"]
            print("Using all threads for synthesis...")
        else:
            try:
                thread_index = int(choice) - 1
                if 0 <= thread_index < len(threads_data["threads"]):
                    selected_threads = [threads_data["threads"][thread_index]]
                    print(f"Selected thread: {selected_threads[0]['title']}")
                else:
                    print("Invalid choice. Using all threads...")
                    selected_threads = threads_data["threads"]
            except ValueError:
                print("Invalid input. Using all threads...")
                selected_threads = threads_data["threads"]

        # --- ADDITIONAL INSTRUCTIONS STEP ---
        print("\nWould you like to add any specific instructions for the video script?")
        print("(e.g., 'Focus more on the environmental impact', 'Make it more personal', 'Add more technical details', etc.)")
        print("Press Enter to skip or type your instructions:")
        additional_instructions = input("Additional instructions: ").strip()

        # --- NEW STEP 2: Synthesize Content with Selected Threads ---
        print("\nStep 2: Synthesizing content from selected threads...")

        # Build input object for synthesis with selected threads and additional instructions
        synthesis_input = {
            "input": question,
            "sources": cleaned_sources,
            "threads": selected_threads,
            "thread_summary": threads_data["summary"],
            "additional_instructions": additional_instructions if additional_instructions else ""
        }

    # Send inference request to synthesis function
    response = client.inference(
        function_name="synthesise_content",
        input={
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "arguments": synthesis_input
                        }
                    ]
                }
            ]
        },
        episode_id=threading_response.episode_id,
    )

    print("\nFinal synthesis complete!")
    print(response)

    # --- FEEDBACK SECTION --
    feedback = input("How useful was this? (1-5): ").strip().lower()

    if feedback.isdigit() and 1 <= int(feedback) <= 5:
        rating = int(feedback)
        
        # Use HTTP client for feedback
        with TensorZeroGateway.build_http(gateway_url="http://localhost:3000") as feedback_client:
            feedback_result = feedback_client.feedback(
                metric_name="user_rating",
                episode_id=threading_response.episode_id,
                value=float(rating),
            )
            print("Feedback recorded:", feedback_result)

    else:
        print("Invalid input. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()