import json
import os
from typing import List
from app.src.models.product import Product
from app.src.config.settings import settings


class PicklistRepository:
    """
    Handles loading and accessing the product picklist from a JSON file.
    """

    def __init__(self, file_path: str = settings.PICKLIST_PATH):
        """
        Initializes the repository with a file path.

        Args:
            file_path: Path to the JSON picklist file.
        """
        self.file_path = file_path

    def load(self) -> List[Product]:
        """
        Loads the picklist from the configured file path.

        Returns:
            A list of Product objects.
        """
        if not os.path.exists(self.file_path):
            print(f"Error: Picklist file not found at {self.file_path}")
            return []

        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
            return [Product.from_dict(item) for item in data]
        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode JSON from {self.file_path}: {e}")
            return []
        except Exception as e:
            print(f"Error loading picklist: {e}")
            return []
