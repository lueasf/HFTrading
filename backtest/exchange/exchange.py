import logging
from typing import Dict

from backtest.exchange.orderbook import OrderBook, Order

logger = logging.getLogger(__name__)


class Exchange:
    def __init__(self, name: str, fee_rate: float, initial_balance: Dict[str, float]):
        self.name = name
        self.fee_rate = fee_rate
        self.balances = initial_balance

        self.order_books: Dict[str, OrderBook] = {}

    def add_order_book(self, symbol: str):
        if symbol not in self.order_books:
            self.order_books[symbol] = OrderBook(symbol)
            logger.debug(f"Order book for {symbol} added to exchange {self.name}.")
        else:
            logger.debug(f"Order book for {symbol} already exists in exchange {self.name}.")

    def get_order_book(self, symbol: str) -> OrderBook | None:
        if symbol in self.order_books:
            return self.order_books[symbol]
        else:
            logger.error(f"Order book for {symbol} not found in exchange {self.name}.")
            return None

    def submit_order(self, order: Order):
        order_book = self.get_order_book(order.symbol)
        if order_book:
            if order.side == "buy":
                order_book.add_bid(order.price, order.quantity)
            else:
                order_book.add_ask(order.price, order.quantity)
            logger.debug(f"Order {order} submitted to exchange {self.name}.")

    def cancel_order(self, order: Order):
        order_book = self.get_order_book(order.symbol)
        if order_book:
            if order.side == "buy":
                order_book.remove_bid(order.price, order.quantity)
            else:
                order_book.remove_ask(order.price, order.quantity)
            logger.debug(f"Order {order} cancelled from exchange {self.name}.")