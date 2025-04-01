import logging
from dataclasses import dataclass
from enum import Enum
from typing import Dict

logger = logging.getLogger(__name__)


class OrderBookLevel:
    def __init__(self, price: float, volume: float):
        self.price = price
        self.volume = volume
        self.orders: Dict[str, Order] = {}


class OrderBook:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.bids: Dict[float, OrderBookLevel] = {}
        self.asks: Dict[float, OrderBookLevel] = {}

    def add_bid(self, price: float, volume: float):
        if price not in self.bids:
            self.bids[price] = OrderBookLevel(price, volume)
        else:
            self.bids[price].volume += volume

    def add_ask(self, price: float, volume: float):
        if price not in self.asks:
            self.asks[price] = OrderBookLevel(price, volume)
        else:
            self.asks[price].volume += volume

    def remove_bid(self, price: float, volume: float):
        if price in self.bids:
            self.bids[price].volume -= volume
            if self.bids[price].volume <= 0:
                del self.bids[price]

    def remove_ask(self, price: float, volume: float):
        if price in self.asks:
            self.asks[price].volume -= volume
            if self.asks[price].volume <= 0:
                del self.asks[price]

    def get_best_bid(self):
        if self.bids:
            return max(self.bids.items(), key=lambda x: x[0])
        return None

    def get_best_ask(self):
        if self.asks:
            return min(self.asks.items(), key=lambda x: x[0])
        return None


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

    @property
    def remaining_quantity(self):
        return self.quantity - self.filled_quantity
