import os
import urllib.request
import zipfile
from abc import ABC, abstractmethod
from typing import List, Iterator, Any, Dict

import clickhouse_connect

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


class DataSource(ABC):
    @abstractmethod
    def get_data(self, start_time: float, end_time: float) -> Iterator[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_symbols(self) -> List[str]:
        pass

    @abstractmethod
    def get_exchanges(self) -> List[str]:
        pass


class NoDataSource(DataSource):
    def get_data(self, start_time: float, end_time: float) -> Iterator[Dict[str, Any]]:
        return iter([])

    def get_symbols(self) -> List[str]:
        return []

    def get_exchanges(self) -> List[str]:
        return []


class ClickHouseDataSource(DataSource):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.table_name = "orders"

        # Initialize the ClickHouse connection
        self.client = clickhouse_connect.get_client(host=connection_string)

    def get_data(self, start_time: float, end_time: float) -> Iterator[Dict[str, Any]]:
        query = f"""
        SELECT * FROM {self.table_name}
        WHERE timestamp >= {start_time} AND timestamp <= {end_time}
        """
        result = self.client.query(query)
        for row in result.result_rows:
            yield dict(zip(result.column_names, row))

    def get_symbols(self) -> List[str]:
        query = f"SELECT DISTINCT symbol FROM {self.table_name}"
        result = self.client.query(query)
        return [row[0] for row in result.result_rows]

    def get_exchanges(self) -> List[str]:
        query = f"SELECT DISTINCT exchange FROM {self.table_name}"
        result = self.client.query(query)
        return [row[0] for row in result.result_rows]


class BinanceAPIDataSource(DataSource):
    def __init__(self, symbol: str, date: str):
        self.api_url = "https://data.binance.vision/data/spot/daily/trades" + "/" + symbol + "/" + symbol + "-trades-" + date + ".zip"
        self.exchange = "Binance"
        self.symbol = symbol
        self.date = date

    def get_data(self, start_time: float, end_time: float) -> Iterator[Dict[str, Any]]:
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
                yield {
                    "trade_id": float(columns[0]),
                    "price": float(columns[1]),
                    "volume": float(columns[2]),
                    "timestamp": float(columns[4]),
                    "is_buyer_maker": bool(columns[5]),
                    "exchange": self.exchange,
                    "symbol": self.symbol
                }

    def get_symbols(self) -> List[str]:
        # Placeholder for actual API call
        return [self.symbol]

    def get_exchanges(self) -> List[str]:
        # Placeholder for actual API call
        return [self.exchange]


class OKXAPIDataSource(DataSource):
    def __init__(self, symbol: str, date: str):
        self.api_url = f"https://www.okx.com/cdn/okex/traderecords/trades/daily/{date.replace('-', '')}/{symbol}-trades-{date}.zip"
        print(self.api_url)
        self.exchange = "OKX"
        self.symbol = symbol
        self.date = date

    def get_data(self, start_time: float, end_time: float) -> Iterator[Dict[str, Any]]:
        # Create folder if it doesn't exist
        os.makedirs(f".data/{self.exchange}", exist_ok=True)

        request = urllib.request.Request(self.api_url, headers=headers)
        # Download the zip file
        response = urllib.request.urlopen(request)
        with open(f".data/{self.exchange}/{self.symbol}-{self.date}.zip", 'wb') as file:
            file.write(response.read())

        #urllib.request.urlretrieve(self.api_url, f".data/{self.exchange}/{self.symbol}-{self.date}.zip")
        # Unzip the file
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
                yield {
                    "trade_id": float(columns[0]),
                    "is_buyer_maker": columns[1] == 'buy',
                    "volume": float(columns[2]),
                    "price": float(columns[3]),
                    "timestamp": float(columns[4]),
                    "exchange": self.exchange,
                    "symbol": self.symbol
                }

    def get_symbols(self) -> List[str]:
        # Placeholder for actual API call
        return [self.symbol]

    def get_exchanges(self) -> List[str]:
        # Placeholder for actual API call
        return [self.exchange]
