import unittest
from backtest.exchange.orderbook import Order, OrderBook, Status


class TestOrder(unittest.TestCase):
    def test_order_creation(self):
        order = Order(
            order_id="test_order_1",
            exchange_name="Test Exchange",
            symbol="BTC-USD",
            price=50000.0,
            quantity=1.0,
            filled_quantity=0.0,
            status=Status.PENDING,
            side="buy"
        )
        
        self.assertEqual(order.order_id, "test_order_1")
        self.assertEqual(order.exchange_name, "Test Exchange")
        self.assertEqual(order.symbol, "BTC-USD")
        self.assertEqual(order.price, 50000.0)
        self.assertEqual(order.quantity, 1.0)
        self.assertEqual(order.filled_quantity, 0.0)
        self.assertEqual(order.status, Status.PENDING)
        self.assertEqual(order.side, "buy")
    
    def test_remaining_quantity(self):
        order = Order(
            order_id="test_order_1",
            exchange_name="Test Exchange",
            symbol="BTC-USD",
            price=50000.0,
            quantity=2.0,
            filled_quantity=0.5,
            status=Status.PARTIALLY_FILLED,
            side="buy"
        )
        
        self.assertEqual(order.remaining_quantity, 1.5)


class TestOrderBook(unittest.TestCase):
    def setUp(self):
        self.order_book = OrderBook("BTC-USD")

        self.assertEqual(self.order_book.symbol, "BTC-USD")
        self.assertEqual(self.order_book.bids, {})
        self.assertEqual(self.order_book.asks, {})
        self.assertEqual(self.order_book.orders, {})
        
        # Add some orders
        self.bid_order1 = Order(
            order_id="bid1",
            exchange_name="Test Exchange",
            symbol="BTC-USD",
            price=49000.0,
            quantity=1.0,
            filled_quantity=0.0,
            status=Status.PENDING,
            side="buy"
        )
        
        self.bid_order2 = Order(
            order_id="bid2",
            exchange_name="Test Exchange",
            symbol="BTC-USD",
            price=50000.0,
            quantity=0.5,
            filled_quantity=0.0,
            status=Status.PENDING,
            side="buy"
        )
        
        self.ask_order1 = Order(
            order_id="ask1",
            exchange_name="Test Exchange",
            symbol="BTC-USD",
            price=51000.0,
            quantity=1.0,
            filled_quantity=0.0,
            status=Status.PENDING,
            side="sell"
        )
        
        self.ask_order2 = Order(
            order_id="ask2",
            exchange_name="Test Exchange",
            symbol="BTC-USD",
            price=52000.0,
            quantity=2.0,
            filled_quantity=0.0,
            status=Status.PENDING,
            side="sell"
        )
    
    def test_add_bid(self):
        self.order_book.add_bid(self.bid_order1)
        self.assertIn(49000.0, self.order_book.bids)
        self.assertEqual(self.order_book.bids[49000.0].volume, 1.0)
        self.assertIn(self.bid_order1.order_id, self.order_book.orders)
        
        # Add another bid at the same price
        another_bid = Order(
            order_id="bid3",
            exchange_name="Test Exchange",
            symbol="BTC-USD",
            price=49000.0,
            quantity=0.5,
            filled_quantity=0.0,
            status=Status.PENDING,
            side="buy"
        )
        self.order_book.add_bid(another_bid)
        self.assertEqual(self.order_book.bids[49000.0].volume, 1.5)
    
    def test_add_ask(self):
        self.order_book.add_ask(self.ask_order1)
        self.assertIn(51000.0, self.order_book.asks)
        self.assertEqual(self.order_book.asks[51000.0].volume, 1.0)
        self.assertIn(self.ask_order1.order_id, self.order_book.orders)
        
        # Add another ask at the same price
        another_ask = Order(
            order_id="ask3",
            exchange_name="Test Exchange",
            symbol="BTC-USD",
            price=51000.0,
            quantity=0.5,
            filled_quantity=0.0,
            status=Status.PENDING,
            side="sell"
        )
        self.order_book.add_ask(another_ask)
        self.assertEqual(self.order_book.asks[51000.0].volume, 1.5)
    
    def test_remove_bid(self):
        self.order_book.add_bid(self.bid_order1)
        self.order_book.remove_bid(self.bid_order1)
        self.assertNotIn(49000.0, self.order_book.bids)
        self.assertNotIn(self.bid_order1.order_id, self.order_book.orders)
    
    def test_remove_ask(self):
        self.order_book.add_ask(self.ask_order1)
        self.order_book.remove_ask(self.ask_order1)
        self.assertNotIn(51000.0, self.order_book.asks)
        self.assertNotIn(self.ask_order1.order_id, self.order_book.orders)
    
    def test_get_best_bid(self):
        # Empty order book
        self.assertEqual(self.order_book.get_best_bid(), (None, None))
        
        # Add bids
        self.order_book.add_bid(self.bid_order1)  # price 49000
        self.order_book.add_bid(self.bid_order2)  # price 50000
        
        best_price, level = self.order_book.get_best_bid()
        self.assertEqual(best_price, 50000.0)  # Highest bid price
    
    def test_get_best_ask(self):
        # Empty order book
        self.assertEqual(self.order_book.get_best_ask(), (None, None))
        
        # Add asks
        self.order_book.add_ask(self.ask_order1)  # price 51000
        self.order_book.add_ask(self.ask_order2)  # price 52000
        
        best_price, level = self.order_book.get_best_ask()
        self.assertEqual(best_price, 51000.0)  # Lowest ask price
    
    def test_match_orders(self):
        # Add orders with crossing prices (bid > ask) to trigger matching
        crossing_bid = Order(
            order_id="crossing_bid",
            exchange_name="Test Exchange",
            symbol="BTC-USD",
            price=52000.0,  # Higher than the ask
            quantity=0.5,
            filled_quantity=0.0,
            status=Status.PENDING,
            side="buy"
        )
        
        crossing_ask = Order(
            order_id="crossing_ask",
            exchange_name="Test Exchange",
            symbol="BTC-USD",
            price=51000.0,
            quantity=0.5,
            filled_quantity=0.0,
            status=Status.PENDING,
            side="sell"
        )
        
        self.order_book.add_bid(crossing_bid)
        self.order_book.add_ask(crossing_ask)
        
        matched_orders = self.order_book.match_orders()

        # Should have matched the crossing bid
        self.assertIn("crossing_bid", matched_orders)
        
        # Verify the match details
        self.assertEqual(matched_orders["crossing_bid"]["price"], 51000.0)
        self.assertEqual(matched_orders["crossing_bid"]["quantity"], 0.5)
    
    def test_export(self):
        self.order_book.add_bid(self.bid_order1)
        self.order_book.add_ask(self.ask_order1)
        
        export_data = self.order_book.export()
        
        self.assertEqual(export_data["symbol"], "BTC-USD")
        self.assertIn(49000.0, export_data["bids"])
        self.assertIn(51000.0, export_data["asks"])
        self.assertEqual(export_data["bids"][49000.0], 1.0)
        self.assertEqual(export_data["asks"][51000.0], 1.0)


if __name__ == "__main__":
    unittest.main()