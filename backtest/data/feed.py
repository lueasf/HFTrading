from abc import ABC, abstractmethod
from typing import Any, Self

from backtest.data.data_source import DataSource, ExchangeData


class DataFeed(ABC):
    @abstractmethod
    def fetch_data(self, data_source: DataSource):
        pass

    @abstractmethod
    def initialize(self, start_time: float, end_time: float) -> Self:
        pass

    @abstractmethod
    def get_events(self) -> list[Any]:
        pass


class ExchangeDataFeed(DataFeed):

    def __init__(self, start_time: float, end_time: float):
        self.start_time = start_time
        self.end_time = end_time
        self.data = None

    def initialize(self, start_time: float, end_time: float) -> Self:
        pass

    def fetch_data(self, data_source: DataSource) -> Self:
        self.data = data_source.get_data(
            start_time=self.start_time, end_time=self.end_time
        )
        return self

    def get_events(self) -> list[ExchangeData]:
        return list(self.data)