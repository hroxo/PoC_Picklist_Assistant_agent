import sys
import time
from app.src.services.file_service import FileService
from app.src.services.ai_service import AIService
from app.src.services.matching_service import MatchingService
from app.src.repositories.picklist_repository import PicklistRepository


def main() -> None:
    """
    Main function to orchestrate the fresh produce recognition agent.
    Refactored to use Clean Architecture principles.
    """

    # 1. Validate Arguments
    try:
        path_to_watch = sys.argv[1]
        print("Path received [✅]")
    except IndexError:
        print("Error: Missing argument.",
              "\nUsage: python3 -m app.main <relative/dir/>")
        return

    # 2. Initialize Components

    # Repository & Data
    picklist_repo = PicklistRepository()
    picklist_products = picklist_repo.load()
    if picklist_products:
        print("Picklist found [✅]")
    else:
        print("Warning: Picklist could not be loaded or is empty.")

    # Services
    ai_service = AIService()
    matching_service = MatchingService(picklist_products)
    file_service = FileService(path_to_watch)

    # 3. Watch Directory
    print(f"Began watching {path_to_watch} [✅]")
    new_image_path = file_service.watch_for_new_file()

    if new_image_path is None:
        print("Error at Watching File")
        return

    # 4. Processing
    latency_start = time.perf_counter()

    try:
        with open(new_image_path, "rb") as file:
            print("Asked Agent for classification [✅]")
            image_bytes = file.read()

            # Retry logic
            while True:
                agent_output = ai_service.analyze_image(image_bytes)
                if "Error" in agent_output and "Exception" in agent_output:
                    print("Error during analysis. Trying again...")
                    time.sleep(1)
                    continue
                break

    except Exception as e:
        print(f"Error reading image: {e}")
        return

    if not agent_output or "Error" in agent_output:
        # Fallback/Error output
        print('{"fruit": "NA", "PLU": "NA", "Price": "NA"}')
        if "Error" in agent_output:
            print(f"Debug: {agent_output}")
        return

    # 5. Matching logic
    print("Analysing our Picklist for suggestion [✅]")

    matches = matching_service.find_matches(agent_output)

    if len(matches) > 1:
        print("Recalling to improve output [✅]")
        refined_output = matching_service.refine_match(ai_service, matches)
        print("List retrieved [✅]")
        # Try to parse the refined output to ensure it's a list or dict
        print(refined_output)
        if not refined_output:
            print("Item not found")

    elif not matches:
        print("Item not found")
        print(f"\nDEBUG MESSAGE:\nAgent output:\n{agent_output}")
    else:
        print("List retrieved [✅]")
        # Output format matching original expectation (list of dicts)
        print([p.to_dict() for p in matches])

    print(f"Latency: {time.perf_counter() - latency_start:.2f} seconds")


if __name__ == "__main__":
    main()
