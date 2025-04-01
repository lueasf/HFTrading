# Backtest Explanation

## Reporters
### Risk
- **VaR** : Value at Risk is a statistical measure that estimates the maximum potential loss a portfolio could face over a specified time period at a given confidence level.
The confidence level is typically set at 95%, meaning that there is a 5% chance that the actual loss will exceed the VaR estimate.
VaR = μ - z * σ
Where:
  - μ is the mean of the returns
  - z is the confidence level
  - σ is the volatility of the returns

Or this formula supposes that the returns are normally distributed.
The percentile use directly the historical data.
95% of confidence means we look at the 5% worst case, thus :
(1 - confidence) * 100 

FYI : Percentile is like a threshold.
10 notes of students :
[5, 10, 10, 11, 12, 13, 14, 15, 16, 20]
P(10% = 1 student) = 5, because 10% of the students (1) got 5 or less.
Thus, np.percentile(self.returns, 5).

- **CVaR** : Conditional Value at Risk is a risk measure that calculate the mean of the losses, that
outperforms the VaR threshold.

- **Sharpe Ratio** : Measures the return compared to the risk.
If SR > 1, the strategy is good.

### Performance (Measure gain)
- **Cumulative Return** : shows how much the portfolio has grown over time.
- **Win Rate** : the percentage of trades that were profitable.