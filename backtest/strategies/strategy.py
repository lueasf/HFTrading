from abc import abstractmethod


class Strategy:
    def __init__(self, data_feed, exchange):
        """
        Init strategy
        :param data_feed: data from data source
        :param exchange: exchange to trade on
        """
        self.data_feed = data_feed
        self.exchange = exchange

    @abstractmethod
    def generate_orders(self):
        pass