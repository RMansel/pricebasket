from dataclasses import dataclass
from math import ceil
from typing import Dict


@dataclass()
class Discount:
    description: str

    def savings(self, prices: Dict[str, int], basket: Dict[str, int]) -> float:
        raise NotImplementedError


@dataclass()
class BuySomeGetMoneyOff(Discount):
    trigger_item: str
    discount_item: str
    trigger_num: int
    discount_num: int
    discount_rate: float

    def savings(self, prices: Dict[str, int], basket: Dict[str, int]) -> float:
        """

        Args:
            prices (): A dict of product -> price
            basket (): A dict of product -> quantity

        Returns: The total applicable discount

        """
        triggers = basket.get(self.trigger_item, 0) // self.trigger_num
        discounts = triggers * self.discount_num
        valid_items = min(discounts, basket.get(self.discount_item, 0))
        savings = valid_items * self.discount_rate * prices[self.discount_item]
        return ceil(savings)


@dataclass()
class FlatDiscount(Discount):
    discount_item: str
    discount_rate: float

    def savings(self, prices: Dict[str, int], basket: Dict[str, int]) -> float:
        """

        Args:
            prices (): A dict of product -> price
            basket (): A dict of product -> quantity

        Returns: The total applicable discount

        """
        savings = basket.get(self.discount_item, 0) * prices[self.discount_item] * self.discount_rate
        return ceil(savings)
