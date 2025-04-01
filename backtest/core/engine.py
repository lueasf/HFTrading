import logging
from typing import Dict, Any, List

from backtest.data.feed import DataFeed
from backtest.exchange.exchange import Exchange

logger = logging.getLogger(__name__)


class BacktestEngine:

    def __init__(self, start_time: float, end_time: float):
        self.start_time = start_time
        self.end_time = end_time
        self.current_time = start_time
        self.is_running = False

        self.exchanges: Dict[str, Exchange] = {}

        self.data_feeds: List[DataFeed] = []

        self.events: Dict[float, Any] = {}
        self.timestamps = []

    def add_exchange(self, exchange: Exchange):
        self.exchanges[exchange.name] = exchange
        logger.debug("Exchange added: %s", exchange.name)

    def add_data_feed(self, data_feed):
        self.data_feeds.append(data_feed)
        logger.debug("Data feed added: %s", data_feed)

    def initialize(self):
        for data_feed in self.data_feeds:
            data_feed.initialize(self.start_time, self.end_time)
            logger.debug("Data feed initialized: %s", data_feed)

        # Initialize events and timestamps
        for data_feed in self.data_feeds:
            for timestamp, event in data_feed.get_events():
                self.events[timestamp] = event
                self.timestamps.append(timestamp)

        self.timestamps = list(set(self.timestamps))
        self.timestamps.sort()

    def process_next_event(self):
        if self.current_time in self.events:
            event = self.events[self.current_time]
            exchange = self.exchanges.get(event["exchange"])
            if exchange:
                exchange.submit_order(event["order"])
            else:
                logger.error("Exchange not found for event: %s", event)
        else:
            self.current_time = self.timestamps.pop(0) if self.timestamps else None

    def run(self):
        logger.info("Backtest started from %s to %s", self.start_time, self.end_time)
        self.is_running = True

        while self.current_time < self.end_time:
            # TODO: Implement the backtest logic here
            self.current_time += 1  # Increment time for the sake of example
        logger.info("Backtest completed")
