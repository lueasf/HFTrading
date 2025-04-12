from backtest.exchange.orderbook import Order, Status
from backtest.strategies.strategy import Strategy


class StaticArbitrageStrategy(Strategy):
    def __init__(self, data_feed_1, data_feed2, exchange_1, exchange_2, spread=0.01, threshold=0.01):
        super().__init__(data_feed_1, exchange_1)
        self.data_feed1 = data_feed_1
        self.data_feed2 = data_feed2
        self.exchange1 = exchange_1
        self.exchange2 = exchange_2
        self.threshold = threshold
        self.spread = spread

    def generate_orders(self):
        price_1 = self.data_feed1.get_best_bid()
        price_2 = self.data_feed2.get_best_ask()

        if price_2 - price_1 > self.threshold:

            buy_order = Order(
                order_id="buy_order_1",
                exchange_name=self.exchange_1.name,
                symbol=self.data_feed_1.symbol,
                price=price_1,
                quantity=self.order_size,
                filled_quantity=0.0,
                status=Status.PENDING,
                side="buy"
            )

            sell_order = Order(
                order_id="sell_order_1",
                exchange_name=self.exchange_2.name,
                symbol=self.data_feed_2.symbol,
                price=price_2,
                quantity=self.order_size,
                filled_quantity=0.0,
                status=Status.PENDING,
                side="sell"
            )

            self.exchange_1.submit_order(buy_order)
            self.exchange_2.submit_order(sell_order)

        elif price_1 - price_2 > self.threshold:

            buy_order = Order(
                order_id="buy_order_2",
                exchange_name=self.exchange_2.name,
                symbol=self.data_feed_2.symbol,
                price=price_2,
                quantity=self.order_size,
                filled_quantity=0.0,
                status=Status.PENDING,
                side="buy"
            )

            sell_order = Order(
                order_id="sell_order_2",
                exchange_name=self.exchange_1.name,
                symbol=self.data_feed_1.symbol,
                price=price_1,
                quantity=self.order_size,
                filled_quantity=0.0,
                status=Status.PENDING,
                side="sell"
            )

            self.exchange_2.submit_order(buy_order)
            self.exchange_1.submit_order(sell_order)

        else :
            print("No arbitrage opportunity found.")


if __name__ == "__main__":
    pass