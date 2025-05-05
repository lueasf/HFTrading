import logging
from dataclasses import dataclass
from enum import Enum
from typing import Dict

from backtest.data.data_source import ExchangeData

logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING = "pending"
    OPEN = "open"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELED = "canceled"
    REJECTED = "rejected"


@dataclass
class Order:
    order_id: str
    exchange_name: str
    symbol: str
    price: float
    quantity: float
    filled_quantity: float
    status: Status
    side: str
    callback: callable = lambda x: None

    @property
    def remaining_quantity(self):
        return self.quantity - self.filled_quantity

    @classmethod
    def from_exchangedata(cls, exchange_data: ExchangeData):
        return cls(
            order_id=str(exchange_data.trade_id),
            exchange_name=exchange_data.exchange,
            symbol=exchange_data.symbol,
            price=exchange_data.price,
            quantity=exchange_data.volume,
            filled_quantity=0.0,
            status=Status.PENDING,
            side="buy" if exchange_data.is_buyer_maker else "sell"
        )

    def __repr__(self):
        return f"Order(order_id={self.order_id}, exchange_name={self.exchange_name}, symbol={self.symbol}, price={self.price}, quantity={self.quantity}, filled_quantity={self.filled_quantity}, status={self.status}, side={self.side})"


class OrderBookLevel:
    def __init__(self, price: float, volume: float):
        self.price = price
        self.volume = volume
        self.orders: Dict[str, Order] = {}

    def __repr__(self):
        return f"OrderBookLevel(price={self.price}, volume={self.volume}, orders={self.orders})"


class OrderBook:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.bids: Dict[float, OrderBookLevel] = {}
        self.asks: Dict[float, OrderBookLevel] = {}

        self.orders: Dict[str, Order] = {}

    def export(self) -> dict:
        return {
            "symbol": self.symbol,
            "bids": {price: level.volume for price, level in self.bids.items()},
            "asks": {price: level.volume for price, level in self.asks.items()},
        }

    def add_bid(self, order: Order):
        price = order.price
        volume = order.quantity
        if price not in self.bids:
            self.bids[price] = OrderBookLevel(price, volume)
        else:
            self.bids[price].volume += volume

        self.bids[price].orders[order.order_id] = order
        self.orders[order.order_id] = order

    def add_ask(self, order: Order):
        price = order.price
        volume = order.quantity
        if price not in self.asks:
            self.asks[price] = OrderBookLevel(price, volume)
        else:
            self.asks[price].volume += volume

        self.asks[price].orders[order.order_id] = order
        self.orders[order.order_id] = order

    def remove_bid(self, order: Order):
        price = order.price
        volume = order.quantity
        if price in self.bids:
            self.bids[price].volume -= volume
            if order.order_id in self.bids[price].orders:
                del self.bids[price].orders[order.order_id]
            if self.bids[price].volume <= 0:
                del self.bids[price]

        if order.order_id in self.orders:
            del self.orders[order.order_id]

    def remove_ask(self, order: Order):
        price = order.price
        volume = order.quantity
        if price in self.asks:
            self.asks[price].volume -= volume
            if self.asks[price].volume <= 0:
                del self.asks[price]

        if order.order_id in self.orders:
            del self.orders[order.order_id]

    def get_best_bid(self):
        if self.bids:
            return max(self.bids.items(), key=lambda x: x[0])
        return None, None

    def get_best_ask(self) -> tuple[float, OrderBookLevel] | tuple[None, None]:
        if self.asks:
            return min(self.asks.items(), key=lambda x: x[0])
        return None, None

    def match_orders(self) -> Dict[str, Dict[str, float]]:
        matched_orders = {}

        # Match crossing orders
        best_bid, bid_devel = self.get_best_bid()
        best_ask, ask_devel = self.get_best_ask()

        if best_bid is not None and best_ask is not None and best_bid >= best_ask:
            bid_orders = bid_devel.orders.copy()
            ask_orders = ask_devel.orders.copy()

            while bid_orders and ask_orders:
                bid_order = next(iter(bid_orders.values()))
                ask_order = next(iter(ask_orders.values()))

                if bid_order.remaining_quantity > 0 and ask_order.remaining_quantity > 0:
                    matched_quantity = min(
                        bid_order.remaining_quantity, ask_order.remaining_quantity
                    )

                    matched_orders[bid_order.order_id] = {
                        "price": best_ask,
                        "quantity": matched_quantity,
                    }

                    bid_order.filled_quantity += matched_quantity
                    ask_order.filled_quantity += matched_quantity

                    if bid_order.remaining_quantity == 0:
                        del bid_orders[bid_order.order_id]
                    if ask_order.remaining_quantity == 0:
                        del ask_orders[ask_order.order_id]

        return matched_orders
