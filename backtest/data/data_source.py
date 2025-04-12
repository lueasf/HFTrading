import os
import urllib.request
import zipfile
from abc import ABC, abstractmethod
from typing import List, Iterator, Any, Dict

import clickhouse_connect
import csv

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


class ExchangeData:
    def __init__(self, exchange: str, symbol: str, trade_id: float, price: float, volume: float, timestamp: float,
                 is_buyer_maker: bool):
        self.exchange = exchange
        self.symbol = symbol
        self.trade_id = trade_id
        self.price = price
        self.volume = volume
        self.timestamp = timestamp
        self.is_buyer_maker = is_buyer_maker

    def __repr__(self):
        return f"ExchangeData(exchange={self.exchange}, symbol={self.symbol}, trade_id={self.trade_id}, price={self.price}, volume={self.volume}, timestamp={self.timestamp}, is_buyer_maker={self.is_buyer_maker})"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ExchangeData':
        return cls(
            exchange=data.get("exchange"),
            symbol=data.get("symbol"),
            trade_id=data.get("trade_id"),
            price=data.get("price"),
            volume=data.get("volume"),
            timestamp=data.get("timestamp"),
            is_buyer_maker=data.get("is_buyer_maker")
        )


class DataSource(ABC):
    @abstractmethod
    def get_data(self, start_time: float, end_time: float) -> Iterator[ExchangeData]:
        pass

    @abstractmethod
    def get_symbols(self) -> List[str]:
        pass

    @abstractmethod
    def get_exchanges(self) -> List[str]:
        pass


class NoDataSource(DataSource):
    def get_data(self, start_time: float, end_time: float) -> Iterator[ExchangeData]:
        return iter([])

    def get_symbols(self) -> List[str]:
        return []

    def get_exchanges(self) -> List[str]:
        return []


class BinanceAPIDataSource(DataSource):
    def __init__(self, symbol: str, date: str):
        self.api_url = "https://data.binance.vision/data/spot/daily/trades" + "/" + symbol + "/" + symbol + "-trades-" + date + ".zip"
        self.exchange = "Binance"
        self.symbol = symbol
        self.date = date

    def get_data(self, start_time: float, end_time: float) -> Iterator[ExchangeData]:
        # Create folder if it doesn't exist
        os.makedirs(f".data/{self.exchange}", exist_ok=True)

        urllib.request.urlretrieve(self.api_url, f".data/{self.exchange}/{self.symbol}-{self.date}.zip")
        # Unzip the file
        print(f".data/{self.exchange}/{self.symbol}-{self.date}.zip")
        with zipfile.ZipFile(f".data/{self.exchange}/{self.symbol}-{self.date}.zip", 'r') as zip_ref:
            zip_ref.extractall(f".data/{self.exchange}/{self.symbol}-{self.date}")

        # Read the CSV file
        csv_file = f".data/{self.exchange}/{self.symbol}-{self.date}/"
        for filename in os.listdir(csv_file):
            if filename.endswith(".csv"):
                csv_file += filename
                break
        with open(csv_file, 'r') as file:
            for line in file:
                columns = line.strip().split(',')
                yield ExchangeData.from_dict({
                    "trade_id": float(columns[0]),
                    "price": float(columns[1]),
                    "volume": float(columns[2]),
                    "timestamp": float(columns[4]),
                    "is_buyer_maker": bool(columns[5]),
                    "exchange": self.exchange,
                    "symbol": self.symbol
                })

    def get_symbols(self) -> List[str]:
        return [self.symbol]

    def get_exchanges(self) -> List[str]:
        return [self.exchange]


class OKXAPIDataSource(DataSource):
    def __init__(self, symbol: str, date: str):
        self.api_url = f"https://www.okx.com/cdn/okex/traderecords/trades/daily/{date.replace('-', '')}/{symbol}-trades-{date}.zip"
        self.exchange = "OKX"
        self.symbol = symbol
        self.date = date

    def get_data(self, start_time: float, end_time: float) -> Iterator[ExchangeData]:
        # Create folder if it doesn't exist
        os.makedirs(f".data/{self.exchange}", exist_ok=True)

        request = urllib.request.Request(self.api_url, headers=headers)
        # Download the zip file
        response = urllib.request.urlopen(request)
        with open(f".data/{self.exchange}/{self.symbol}-{self.date}.zip", 'wb') as file:
            file.write(response.read())

        # Unzip the file
        with zipfile.ZipFile(f".data/{self.exchange}/{self.symbol}-{self.date}.zip", 'r') as zip_ref:
            zip_ref.extractall(f".data/{self.exchange}/{self.symbol}-{self.date}")

        # Read the CSV file
        csv_file = f".data/{self.exchange}/{self.symbol}-{self.date}/"
        for filename in os.listdir(csv_file):
            if filename.endswith(".csv"):
                csv_file += filename
                break
        with open(csv_file, 'r', encoding='gbk') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                yield ExchangeData.from_dict({
                    "trade_id": float(row[0]),
                    "is_buyer_maker": row[1].lower() == 'buy',
                    "volume": float(row[2]),
                    "price": float(row[3]),
                    "timestamp": float(row[4]),
                    "exchange": self.exchange,
                    "symbol": self.symbol,
                })

    def get_symbols(self) -> List[str]:
        return [self.symbol]

    def get_exchanges(self) -> List[str]:
        return [self.exchange]
