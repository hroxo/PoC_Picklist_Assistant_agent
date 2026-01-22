from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Product:
    """
    Represents a product with fruit name, PLU code, and price.
    """
    fruit: str
    plu: int
    price: float

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Product':
        """
        Creates a Product instance from a dictionary.

        Args:
            data: A dictionary containing 'fruit', 'PLU', and 'Price' keys.

        Returns:
            A new Product instance.
        """
        return cls(
            fruit=data.get("fruit", "Unknown"),
            plu=int(data.get("PLU", 0)),
            price=float(data.get("Price", 0.0))
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Product instance back to a dictionary.

        Returns:
            A dictionary representation of the product.
        """
        return {
            "fruit": self.fruit,
            "PLU": self.plu,
            "Price": self.price
        }
