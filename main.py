from sys import argv

import click

from pricebasket.basket import Basket
from pricebasket.prices.default import default_prices
from pricebasket.offers.default import default_offers


def cli():
    args = [str(arg) for arg in argv[1::]]
    basket = Basket(items=args, prices=default_prices(), offers=default_offers())
    price = basket.checkout()
    click.echo(price)
