import numpy as np

# Measure the effectiveness of the strategy

def interpret_cumulative_returns(cum_return):
    if cum_return > 0.5:
        return "Excellent cumulative return (> 50%)"
    elif cum_return > 0.2:
        return "Good performance (20% - 50%)"
    elif cum_return > 0:
        return "Positive return, but could be improved"
    else:
        return "Negative return, underperformance"

def interpret_win_rate(win_rate):
    if win_rate > 0.75:
        return "High win rate (> 75%)"
    elif win_rate > 0.5:
        return "Moderate win rate (50% - 75%)"
    elif win_rate > 0.25:
        return "Low win rate (25% - 50%)"
    else:
        return "Very low win rate (< 25%)"

def interpret_win_rate_and_risk(win_rate, risk_reward_ratio):
    if win_rate >= 0.6:
        return "Profitable"

    elif win_rate >= 0.5:
        if risk_reward_ratio >= 2.0:
            return "Profitable"
        else:
            return "Break-even"

    elif win_rate >= 0.4:
        if risk_reward_ratio >= 2.0:
            return "Profitable"
        else:
            return "Not Profitable"

    elif win_rate >= 0.3:
        if risk_reward_ratio >= 3.0:
            return "Profitable"
        else:
            return "Not Profitable"

    else:
        if risk_reward_ratio >= 5.0:
            return "Profitable"
        elif risk_reward_ratio == 4.0:
            return "Break-even"
        else:
            return "Not Profitable"

class PerformanceMetrics:
    def __init__(self, returns, pnl, trades):
        self.returns = np.array(returns) # Daily returns (USD)
        self.pnl = np.array(pnl) # Profit and Loss (USD)
        self.trades = trades # Number of trades executed

    def cumulative_returns(self):
        return np.cumprod(1 + self.returns) - 1

    def win_rate(self):
        wins = sum(1 for trade in self.trades if trade['pnl'] > 0)
        total_trades = len(self.trades)
        if total_trades > 0:
            return wins / total_trades
        return 0.0