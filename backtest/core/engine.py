import logging
from typing import Dict, Any, List

from backtest.data.feed import DataFeed
from backtest.exchange.exchange import Exchange

from backtest.reporters.performance import PerformanceMetrics, interpret_win_rate, interpret_cumulative_returns
from backtest.reporters.risk import RiskMetrics, interpret_value_at_risk, interpret_conditional_value_at_risk, interpret_sharpe_ratio


logger = logging.getLogger(__name__)


class BacktestEngine:

    def __init__(self, start_time: float, end_time: float):
        self.start_time = start_time
        self.end_time = end_time
        self.current_time = start_time
        self.is_running = False

        self.returns = []
        self.pnl = []
        self.trades = []

        self.exchanges: Dict[str, Exchange] = {}

        self.data_feeds: List[DataFeed] = []

        self.events: Dict[float, Any] = {}
        self.timestamps = []

    def add_exchange(self, exchange: Exchange):
        self.exchanges[exchange.name] = exchange
        logger.debug("Exchange added: %s", exchange.name)

    def add_data_feed(self, data_feed: DataFeed):
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
                trade = exchange.submit_order(event["order"])

                if trade:
                    self.returns.append(trade["return"])
                    self.pnl.append(trade["pnl"])
                    self.trades.append(trade)
            else:
                logger.error("Exchange not found for event: %s", event)
        else:
            self.current_time = self.timestamps.pop(0) if self.timestamps else None

    def run(self):
        logger.info("Backtest started from %s to %s", self.start_time, self.end_time)
        self.is_running = True

        while self.current_time < self.end_time:
            # TODO: Implement the backtest logic here
            self.process_next_event()
            self.current_time += 1  # Increment time for the sake of example
        logger.info("Backtest completed")
        self.evaluate_perf() # Evaluate Perf

    # Evaluate performance metrics
    def evaluate_perf(self):
        if not self.returns:
            logger.warning("No returns to evaluate")
            return

        # Perf metrics
        metrics = PerformanceMetrics(self.returns, self.pnl, self.trades)

        cumulative_return = metrics.cumulative_returns()[-1] # get last data from the tab
        win_rate = metrics.win_rate()

        cum_return_interp = interpret_cumulative_returns(cumulative_return)
        win_rate_interp = interpret_win_rate(win_rate)

        logger.info("Cumulative return: %s", cum_return_interp)
        logger.info("Win rate: %s", win_rate_interp)
        logger.info("Number of trades: %s", len(self.trades))

        # Risk metrics
        risk_metrics = RiskMetrics(self.returns, self.pnl)
        var = risk_metrics.value_at_risk()
        cvar = risk_metrics.conditional_value_at_risk()
        sharpe = risk_metrics.sharpe_ratio()

        var_interp = interpret_value_at_risk(var)
        cvar_interp = interpret_conditional_value_at_risk(cvar)
        sharpe_interp = interpret_sharpe_ratio(sharpe)

        logger.info("Risk Metrics:")
        logger.info("Value at Risk (VaR): %.4f (%s)", var, var_interp)
        logger.info("Conditional Value at Risk (CVaR): %.4f (%s)", cvar, cvar_interp)
        logger.info("Sharpe Ratio: %.4f (%s)", sharpe, sharpe_interp)