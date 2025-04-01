from backtest.core.engine import BacktestEngine
from backtest.data.data_source import ClickHouseDataSource, BinanceAPIDataSource, OKXAPIDataSource
from backtest.exchange.exchange import Exchange

def run_backtest():
    date = "2025-03-31"

    backtest_engine = BacktestEngine(start_time=0, end_time=100)

    binance_data_source = BinanceAPIDataSource("BTCUSDT", date)
    #print(list(binance_data_source.get_data(0, 0)))
    okx_data_source = OKXAPIDataSource("BTC-USDT", date)
    print(list(okx_data_source.get_data(0, 0)))

    backtest_engine.add_exchange(Exchange("Binance", 0, {"BTC": 100}))
    backtest_engine.add_exchange(Exchange("OKX", 0, {"BTC": 100}))

    #backtest_engine.run()

if __name__ == "__main__":
    run_backtest()
