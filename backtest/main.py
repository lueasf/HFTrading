import logging

from backtest.core.engine import BacktestEngine
from backtest.data.data_source import BinanceAPIDataSource, OKXAPIDataSource
from backtest.data.feed import ExchangeDataFeed
from backtest.exchange.exchange import Exchange

logger = logging.getLogger(__name__)

def run_backtest():
    date = "2025-03-31"
    start_time = 1743379200029404
    end_time = 1743465599970596

    backtest_engine = BacktestEngine(start_time, end_time)

    binance_data_source = BinanceAPIDataSource("BTCUSDT", date)
    #print(list(binance_data_source.get_data(0, 0)))
    okx_data_source = OKXAPIDataSource("BTC-USDT", date)
    #print(list(okx_data_source.get_data(0, 0)))

    backtest_engine.add_exchange(Exchange("Binance", 0, {"BTC": 100}))
    backtest_engine.add_exchange(Exchange("OKX", 0, {"BTC": 100}))

    backtest_engine.add_data_feed(ExchangeDataFeed(start_time, end_time).fetch_data(binance_data_source))
    backtest_engine.add_data_feed(ExchangeDataFeed(start_time, end_time).fetch_data(okx_data_source))

    backtest_engine.run()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    run_backtest()
