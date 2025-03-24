# Momentum-Trading-Algo 

Overview

This algorithm implements a momentum-based trading strategy that selects the top-performing stocks from a given list over a predefined lookback period. The selected stocks are held for a fixed holding period before reassessing and rebalancing the portfolio. The backtest evaluates the strategy's performance over a specified time range.

Strategy Details

Lookback Period: 10 days

Holding Period: 5 days

Top N Stocks: 3

Initial Portfolio Value: $10,000

Trading Universe: AAPL, MSFT, GOOGL, AMZN, NVDA, TSLA, META

Backtest Period: January 1, 2023 - March 20, 2025

How It Works

Fetch historical stock price data using yfinance.

Compute momentum as the percentage return over the lookback period.

Select the top N stocks with the highest momentum.

Sell any previously held stocks at the end of the holding period.

Allocate equal capital to the newly selected top N stocks.

Repeat the process iteratively through the backtest period.

Track portfolio value and visualize results.


Requirements

This script requires the following Python libraries:

yfinance

pandas

numpy

matplotlib

Install them using:

pip install yfinance pandas numpy matplotlib

Running the Algorithm

Execute the script in a Python environment to run the backtest and visualize the portfolio performance:

python momentum_trading.py

Output

Console Logs: Displays selected top performers, buy/sell transactions, and final portfolio value.

Plot: Shows the portfolio value over time.

Performance Metrics: Initial and final portfolio value, total return percentage.

Results Example

2023-01-15: Top performers - ['NVDA', 'TSLA', 'META']
Bought 10.5 shares of NVDA at $190.00
Bought 12.3 shares of TSLA at $162.00
Bought 15.8 shares of META at $125.00
...
Final Value: $15,200.00
Total Return: 52.00%

Limitations & Considerations

Assumes zero transaction costs and perfect order execution.

Momentum strategies can be sensitive to lookback and holding period selection.

Market conditions (volatility, news events) can affect real-world performance.

Future Enhancements

Include transaction costs and slippage.

Optimize lookback and holding periods using historical performance.

Expand universe to additional sectors or global markets.

Author

Developed by Fahd Sliman
