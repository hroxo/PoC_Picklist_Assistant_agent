import json
from typing import List, Dict, Any
from app.src.models.product import Product
from app.src.services.ai_service import AIService


class MatchingService:
    """
    Service for matching AI output with the product picklist.
    """

    def __init__(self, picklist: List[Product]):
        """
        Initializes the service with a product list.

        Args:
            picklist: List of available products.
        """
        self.picklist = picklist

    def find_matches(self, agent_output: str) -> List[Product]:
        """
        Parses agent output and finds matching products in the picklist.

        Args:
            agent_output: JSON string returned by the agent.

        Returns:
            A list of matching Product objects.
        """
        try:
            agent_json: Dict[str, Any] = json.loads(agent_output)
        except json.JSONDecodeError as e:
            print(f"Error parsing agent output: {e}\n"
                  f"Output was: {agent_output}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []

        target_fruit = str(agent_json.get("fruit", "")).lower()
        if not target_fruit:
            return []

        matches = []
        for product in self.picklist:
            if target_fruit in product.fruit.lower():
                matches.append(product)

        return matches

    def refine_match(self, ai_service: AIService,
                     matches: List[Product]) -> str:
        """
        Asks the AI to pick the best match from a list of candidates.

        Args:
            ai_service: The AI service instance.
            matches: List of candidate products.

        Returns:
            The refined JSON string from the AI.
        """
        matches_json = [p.to_dict() for p in matches]

        new_prompt = (
            f"Re-examine the image. Select the best matching JSON from the "
            f"provided list (confidence threshold: 0.95). "
            f"Return ONLY the JSON object.\n\n"
            f"List: {matches_json}"
        )

        return ai_service.refine_analysis(new_prompt)
