import json


def cross_w_picklist(picklist: str, agent_output: str) -> list:
    """
    Cross-references the agent's classification result with the picklist inventory.

    Args:
        picklist (str): A JSON string representing the list of available items.
        agent_output (str): A JSON string representing the agent's classification output.

    Returns:
        list: A list of dictionaries containing items from the picklist that match
              the agent's classification. Returns an empty list if parsing fails
              or no matches are found.
    """

    try:
        picklist_json: dict = json.loads(picklist)

    except Exception as e:
        print(f"Error picklist_json\n{e}\nNot able to read string to json")
        return []

    try:
        agent_json: dict = json.loads(agent_output)
    except Exception as e:
        print(f"Error agent_json\n{e}\nNot able to read string to json")
        print(f"\nDEBUG MESSAGE:\n{agent_output}\n\n")
        return []

    item_found = []

    for item in picklist_json:
        if str(agent_json["fruit"]).lower() in str(item["fruit"]).lower():
            item_found.append(item)

    return item_found
