from processor.FileHandler import FileHandler
from agent.brain import Agent
from processor.searcher import cross_w_picklist
import sys
import time
import os
from dotenv import load_dotenv


def main() -> None:
    """
    Main function to orchestrate the fresh produce recognition agent.

    It performs the following steps:
    1. Validates CLI arguments.
    2. Loads the picklist from a JSON file.
    3. Initializes the file watcher for the specified directory.
    4. Upon detecting a new image, sends it to the AI agent for classification.
    5. Cross-references the agent's output with the picklist.
    6. Prints the results and processing latency.
    """

    load_dotenv()
    prompt_path = os.getenv("PROMPT")

    if prompt_path is None:
        print("Error\nMake sure you have the correct path to the Prompt in your .env file")
        return
    else:
        str(prompt_path)
    print("Path to PROMPT [✅]")

    agent = Agent(agent_model='gemini-3-flash-preview', prompt=prompt_path)

    try:
        path: str = sys.argv[1]
        print("Path received [✅]")
    except Exception as e:
        print(f"Error {e}",
              "\npython3 main.py <relative/dir/>")
        return

    try:
        with open("processor/picklist.json", 'r') as f:
            picklist = f.read()
        print("Picklist found [✅]")
    except Exception as e:
        print(f"Error {e} opening picklist")

    handler = FileHandler(path)

    image = handler.watch_dir()
    print(f"Began watching {path} [✅]")

    if image is None:
        print("Error at Watching File")
        return

    latencia = time.perf_counter()  # Latencia de processamento

    with open(image, "rb") as file:
        print("Asked Agent for classification [✅]")

        image_read = file.read()

        while True:
            try:
                agent_output = agent.think(image_read)
                break
            except Exception as e:
                print(f"Error {e}\nTrying again")
                time.sleep(1)

    if agent_output is None:
        print('{"fruit": "NA", "PLU": "NA", "Price": "NA"}')
        return

    print("Analysing our Picklist for suggestion [✅]")

    items_found = cross_w_picklist(picklist=picklist,
                                   agent_output=agent_output)

    if items_found != []:
        print("List retrieved [✅]")
        print(items_found,
              f"Latency: {time.perf_counter() - latencia:.2f} seconds")
    else:
        print("Item not found")


if __name__ == "__main__":
    main()
