from typing import List

from pricebasket.discounts import BuySomeGetMoneyOff, FlatDiscount, Discount


def default_offers() -> List[Discount]:
    return [
        BuySomeGetMoneyOff(
            description="Buy 2 soup, get bread half price",
            trigger_item="SOUP",
            discount_item="BREAD",
            trigger_num=2,
            discount_num=1,
            discount_rate=0.5
        ),
        FlatDiscount(
            description="Apples 10% off",
            discount_item="APPLES",
            discount_rate=0.1
        )
    ]

