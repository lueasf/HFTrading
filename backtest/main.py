from backtest.core.engine import BacktestEngine
from backtest.data.data_source import ClickHouseDataSource
from backtest.exchange.exchange import Exchange


def run_backtest():
    backtest_engine = BacktestEngine(start_time=0, end_time=100)

    backtest_engine.add_data_feed(ClickHouseDataSource(connection_string="localhost"))

    backtest_engine.add_exchange(Exchange("Binance", 0, {"BTC": 100}))
    backtest_engine.add_exchange(Exchange("OKX", 0, {"BTC": 100}))

    backtest_engine.run()

if __name__ == "__main__":
    run_backtest()
