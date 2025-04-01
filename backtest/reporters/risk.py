import numpy as np

# Asses the risk
def interpret_value_at_risk(var):
    if var > -0.03:
        return "Low risk, losses are unlikely to exceed 3%"
    elif var > -0.05:
        return "Moderate risk, losses are unlikely to exceed 5%"
    else :
        return "High risk, losses are likely to exceed 5%"

def interpret_conditional_value_at_risk(cvar):
    if cvar > -0.07:
        return "excellent CVaR."
    elif cvar > -0.12:
        return "CVaR is acceptable. "
    else:
        return "Poor CVaR signals potential for catastrophic losses (>12%)"

def interpret_sharpe_ratio(sharpe_ratio):
    if sharpe_ratio > 1:
        return "Good Sharpe Ratio (> 1)"
    elif sharpe_ratio > 0:
        return "Acceptable Sharpe Ratio (0 to 1)"
    else:
        return "Poor Sharpe Ratio (< 0)"

class RiskMetrics:
    def __init__(self, returns, prices):
        self.returns = np.array(returns)
        self.prices = np.array(prices)

    # Calculate the VaR
    def value_at_risk(self, confidence_level=0.95):
        if len(self.returns) == 0:
            raise ValueError("Returns array is empty.")
        var = np.percentile(self.returns, (1 - confidence_level) * 100)
        return var

    # Calculate the CVaR
    def conditional_value_at_risk(self, confidence_level=0.95):
        if len(self.returns) == 0:
            raise ValueError("Returns array is empty.")
        var = self.value_at_risk(confidence_level)
        cvar = self.returns[self.returns <= var].mean()
        return cvar

    # Calculate the Sharpe Ratio
    def sharpe_ratio(self, risk_free_rate=0.01):
        if len(self.returns) == 0:
            raise ValueError("Returns array is empty.")
        excess_returns = self.returns - risk_free_rate
        return np.mean(excess_returns) / np.std(self.returns)