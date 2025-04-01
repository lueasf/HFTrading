from abc import ABC, abstractmethod
from typing import List, Iterator, Any, Dict

import clickhouse_connect


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
