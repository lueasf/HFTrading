from abc import ABC, abstractmethod
from typing import Any

from backtest.data.data_source import ClickHouseDataSource, DataSource


class DataFeed(ABC):
    @abstractmethod
    def fetch_data(self, data_source: DataSource):
        pass

    def initialize(self, start_time: float, end_time: float):
        pass

    def get_events(self) -> list[tuple[float, Any]]:
        pass


class ExchangeDataFeed(DataFeed):

    def __init__(self, start_time: float, end_time: float):
        self.start_time = start_time
        self.end_time = end_time
        self.data = None

    def fetch_data(self, click_house_data_source: ClickHouseDataSource):
        self.data = click_house_data_source.get_data(
            start_time=self.start_time, end_time=self.end_time
        )

    def get_events(self) -> list[dict[float, Any]]:
        return self.data