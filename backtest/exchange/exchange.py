import logging
from typing import Dict

from backtest.exchange.orderbook import OrderBook, Order, Status

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
        if symbol not in self.order_books:
            self.add_order_book(symbol)

        return self.order_books.get(symbol)

    def submit_order(self, order: Order):
        order_book = self.get_order_book(order.symbol)
        if order_book:
            if order.side == "buy":
                order_book.add_bid(order)
            else:
                order_book.add_ask(order)
            logger.debug(f"Order {order} submitted to exchange {self.name}.")

    def cancel_order(self, order: Order):
        order_book = self.get_order_book(order.symbol)
        if order_book:
            if order.side == "buy":
                order_book.remove_bid(order)
            else:
                order_book.remove_ask(order)
            logger.debug(f"Order {order} cancelled from exchange {self.name}.")

    def match_orders(self):
        for order_book in self.order_books.values():
            logger.debug(f"Processing orders for order book {order_book.symbol} in exchange {self.name}.")

            matched_orders: Dict[str, Dict[str, float]] = order_book.match_orders()

            for order_id, match_info in matched_orders:
                order = order_book.orders[order_id]

                previously_filled = order.filled_quantity
                new_filled = match_info["filled_quantity"] + previously_filled

                order.filled_quantity = new_filled

                if order.filled_quantity >= order.quantity:
                    order.status = Status.FILLED

                    order_book.remove_bid(order) if order.side == "buy" else order_book.remove_ask(order)
                else:
                    order.status = Status.PARTIALLY_FILLED

                logger.debug(f"Order {order_id} matched with filled quantity {order.filled_quantity}.")