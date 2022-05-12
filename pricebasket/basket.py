from typing import List, Dict
from pricebasket.discounts import Discount


class Basket:
    prices: Dict[str, int]
    offers: List[Discount]
    items: Dict[str, int]

    def __init__(self, prices: Dict[str, int], offers: List[Discount], items: List[str] = None):
        """

        Args:
            prices (): A dict of product -> price
            offers (): A list of potential Discounts to apply to this sessions.
            items (): A list of strings to attempt to add to the basket
        """
        if type(prices) is not dict or not all([type(k) is str and type(v) is int for k, v in prices.items()]):
            raise ValueError("'prices' type is invalid.")
        if type(offers) is not list or not all([isinstance(i, Discount) for i in offers]):
            raise ValueError("'offers' type is invalid.")
        if items is not None:
            if type(items) is not list:
                raise ValueError("'items' type is invalid.")
        self.prices = prices
        self.offers = offers
        self.items = {}
        if items:
            for item in items:
                self.add_item(item)

    def add_item(self, item: str):
        """

        Args:
            item (): The item to add to the basket

        """
        if type(item) is not str:
            raise ValueError("item type must be string.")
        item_up = item.upper()
        if self.prices.get(item_up):
            current = self.items.get(item_up, 0)
            self.items.update({item_up: current + 1})
        else:
            raise ValueError(f"'{item}' is not for sale.")

    def get_item(self, item: str) -> int:
        """

        Args:
            item (): The item to check the basket for

        Returns: The current number of the requested item in the basket

        """
        return self.items.get(item.upper(), 0)

    def get_subtotal(self) -> int:
        """

        Returns: The total price of goods in the basket without any discounts

        """
        return sum([self.prices.get(k) * v for k, v in self.items.items()])

    def get_discounts(self) -> Dict[str, int]:
        """

        Returns: A dict of discount description -> total applicable discount

        """
        offers = {offer.description: offer.savings(self.prices, self.items) for offer in self.offers}
        return {k: v for k, v in offers.items() if v}

    def checkout(self) -> str:
        """

        Returns: A multi-line string detailing the total, subtotal and any discounts for the current basket.

        """
        subtotal = self.get_subtotal()
        discounts = self.get_discounts()
        output = [f"Subtotal: {'£{:.2f}'.format(subtotal / 100)}"]
        if discounts:
            total = subtotal - sum(discounts.values())
            for k, v in discounts.items():
                if v < 100:
                    discount_str = f"{k}: {v}p"
                else:
                    discount_str = f"{k}: {'£{:.2f}'.format(v / 100)}"
                output.append(discount_str)
        else:
            total = subtotal
            output.append("(No offers available)")
        output.append(f"Total Price: {'£{:.2f}'.format(total / 100)}")

        return "\n".join(output)
