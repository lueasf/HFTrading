from backtest.exchange.orderbook import Order, Status
from backtest.strategies.strategy import Strategy

class MarketMakingStrategy(Strategy):
    def __init__(self, data_feed, exchange, spread=0.01, order_size=1):
        super().__init__(data_feed, exchange)
        self.spread = spread
        self.order_size = order_size

    def generate_orders(self):
        """
        Generate buy and sell signals based on market data based on spread and order size.
        """
        bid_price = self.data_feed.get_best_bid()
        ask_price = self.data_feed.get_best_ask()

        buy_price = bid_price + self.spread
        sell_price = ask_price - self.spread

        buy_order = Order(
            order_id="buy_order_1",
            exchange_name=self.exchange.name,
            symbol=self.data_feed.symbol,
            price=buy_price,
            quantity=self.order_size,
            filled_quantity=0.0,
            status=Status.PENDING,
            side="buy"
        )

        sell_order = Order(
            order_id="sell_order_1",
            exchange_name=self.exchange.name,
            symbol=self.data_feed.symbol,
            price=sell_price,
            quantity=self.order_size,
            filled_quantity=0.0,
            status=Status.PENDING,
            side="sell"
        )

        self.exchange.submit_order(buy_order)
        self.exchange.submit_order(sell_order)

        return {
            "buy_price": buy_price,
            "sell_price": sell_price,
            "order_size": self.order_size
        }

class TestDataFeed:
    def __init__(self, symbol="BTCUSD", bid_price=10000, ask_price=10010):
        self.symbol = symbol
        self.bid_price = bid_price
        self.ask_price = ask_price

    def get_best_bid(self):
            return self.bid_price

    def get_best_ask(self):
        return self.ask_price


class TestExchange:
    def __init__(self,name="Binance"):
        self.name = name

    def submit_order(self, order: Order):
        print("ok")


if __name__ == "__main__":
    data_feed = TestDataFeed()
    exchange = TestExchange()

    strategy = MarketMakingStrategy(data_feed, exchange)
    res = strategy.generate_orders()

    # print(res)

    assert res["buy_price"] == 10000.01
    assert res["sell_price"] == 10009.99
    assert res["order_size"] == 1