import logging
from typing import Dict, List
import pytest

from pricebasket.discounts import BuySomeGetMoneyOff, FlatDiscount, Discount
from pricebasket.basket import Basket


@pytest.fixture
def valid_prices() -> Dict[str, int]:
    return {
        "SOUP": 65,
        "BREAD": 80,
        "MILK": 130,
        "APPLES": 100
    }


@pytest.fixture
def valid_offers() -> List[Discount]:
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


@pytest.fixture
def valid_items() -> List[str]:
    return ["Bread", "Milk", "Apples", "Soup", "Soup"]


def test___init__(valid_prices, valid_offers, valid_items):
    logging.info("valid instantiation with initial items")
    basket = Basket(prices=valid_prices, offers=valid_offers, items=valid_items)
    assert basket.prices == valid_prices
    assert basket.offers == valid_offers
    for item in set(valid_items):
        count = len([s for s in valid_items if s == item])
        assert basket.get_item(item) == count

    logging.info("valid instantiation without initial items")
    basket = Basket(prices=valid_prices, offers=valid_offers)
    assert basket.items == {}

    logging.info("instantiation raises exceptions on invalid parameters")
    with pytest.raises(ValueError, match="'prices' type is invalid."):
        Basket(prices="foo", offers=valid_offers, items=valid_items)
    with pytest.raises(ValueError, match="'offers' type is invalid."):
        Basket(prices=valid_prices, offers="bar", items=valid_items)
    with pytest.raises(ValueError, match="'items' type is invalid."):
        Basket(prices=valid_prices, offers=valid_offers, items=4)


def test_add_item(valid_prices, valid_offers):
    logging.info("adds item to items dict that isn't already there")
    basket = Basket(prices=valid_prices, offers=valid_offers)
    basket.add_item("bread")
    assert basket.get_item("bread") == 1

    logging.info("increases count of item already present in items dict")
    basket.add_item("bread")
    assert basket.get_item("bread") == 2

    logging.info("raises exceptions on invalid arg type")
    with pytest.raises(ValueError, match="item type must be string."):
        basket.add_item(["bread"])

    logging.info("raises exceptions on arg string not in prices")
    with pytest.raises(ValueError, match="'foo' is not for sale."):
        basket.add_item("foo")


def test_get_subtotal(valid_prices, valid_offers, valid_items):
    basket = Basket(prices=valid_prices, offers=valid_offers, items=valid_items)
    logging.info("produces correct subtotal")
    subtotal = basket.get_subtotal()
    assert subtotal == 440

    logging.info("produces correct subtotal after adding additional items")
    for k, v in valid_prices.items():
        old_subtotal = subtotal
        basket.add_item(k)
        subtotal = basket.get_subtotal()
        assert (subtotal - old_subtotal) == v


def test_get_discounts(valid_prices, valid_offers, valid_items):
    basket = Basket(prices=valid_prices, offers=valid_offers, items=valid_items)
    logging.info("creates dict of all applicable discounts")
    discounts = basket.get_discounts()
    for offer in valid_offers:
        assert discounts.get(offer.description) > 0


def test_checkout(valid_prices, valid_offers, valid_items):
    basket = Basket(prices=valid_prices, offers=valid_offers, items=valid_items)
    logging.info("creates correct checkout output with offers")
    checkout_txt = basket.checkout().split('\n')
    assert checkout_txt[0] == 'Subtotal: £4.40'
    assert checkout_txt[1] == 'Buy 2 soup, get bread half price: 40p'
    assert checkout_txt[2] == 'Apples 10% off: 10p'
    assert checkout_txt[3] == 'Total Price: £3.90'

    logging.info("creates correct checkout output without offers")
    basket = Basket(prices=valid_prices, offers=valid_offers)
    checkout_txt = basket.checkout().split('\n')
    assert checkout_txt[0] == 'Subtotal: £0.00'
    assert checkout_txt[1] == '(No offers available)'
    assert checkout_txt[2] == 'Total Price: £0.00'
