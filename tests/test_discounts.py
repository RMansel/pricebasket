import logging
from typing import Dict

import pytest

from pricebasket.discounts import BuySomeGetMoneyOff, FlatDiscount


@pytest.fixture
def valid_prices() -> Dict[str, int]:
    return {
        "SOUP": 65,
        "BREAD": 80,
        "MILK": 130,
        "APPLES": 100
    }


def test_buy_some_get_money_off(valid_prices):
    logging.info("return value of BuySomeGetMoneyOff::savings is correct")
    discount = BuySomeGetMoneyOff(
        description="Buy 2 soup, get bread half price",
        trigger_item="SOUP",
        discount_item="BREAD",
        trigger_num=2,
        discount_num=1,
        discount_rate=0.5
    )
    assert discount.savings(valid_prices, {"SOUP": 2, "BREAD": 1}) == 40
    assert discount.savings(valid_prices, {"SOUP": 3, "BREAD": 1}) == 40
    assert discount.savings(valid_prices, {"SOUP": 1, "BREAD": 1}) == 0
    assert discount.savings(valid_prices, {"SOUP": 4, "BREAD": 2}) == 80
    assert discount.savings(valid_prices, {"SOUP": 4, "BREAD": 3}) == 80
    assert discount.savings(valid_prices, {"SOUP": 2, "BREAD": 1, "FOO": 10}) == 40
    assert discount.savings(valid_prices, {"SOUP": 2, "BREAD": 1, 40: 10}) == 40
    assert discount.savings(valid_prices, {"SOUP": 2, "FOO": 10}) == 0
    assert discount.savings(valid_prices, {"BREAD": 2, "FOO": 10}) == 0

    discount = BuySomeGetMoneyOff(
        description="Buy 2 soup, get bread half price",
        trigger_item="SOUP",
        discount_item="BREAD",
        trigger_num=3,
        discount_num=1,
        discount_rate=0.25
    )
    assert discount.savings(valid_prices, {"SOUP": 2, "BREAD": 1}) == 0
    assert discount.savings(valid_prices, {"SOUP": 3, "BREAD": 1}) == 20


def test_flat_discount(valid_prices):
    logging.info("return value of FlatDiscount::savings is correct")
    discount = FlatDiscount(
        description="Apples 10% off",
        discount_item="APPLES",
        discount_rate=0.1
    )
    for i in range(100):
        res = i * valid_prices[discount.discount_item] * discount.discount_rate
        assert discount.savings(valid_prices, {"APPLES": i}) == res
    assert discount.savings(valid_prices, {"APPLES": 1, "Foo": 1}) == 10
    discount = FlatDiscount(
        description="Apples 10% off",
        discount_item="APPLES",
        discount_rate=0.2
    )
    assert discount.savings(valid_prices, {"APPLES": 1, "Foo": 1}) == 20
