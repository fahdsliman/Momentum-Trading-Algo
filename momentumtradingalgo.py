import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Parameters 
LOOKBACK_PERIOD = 10  # Days to calculate momentum
HOLDING_PERIOD = 5  # Days to hold positions
TOP_N = 3  # Number of top performers to buy
START_DATE = "2023-01-01"
END_DATE = "2025-03-20"  # Up to current date (March 20, 2025)

# List of tickers (e.g., tech stocks)
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META"]


# Fetch historical data
def get_data(tickers, start, end):
    data = yf.download(tickers, start=start, end=end, group_by="ticker")
    return data


# Calculate momentum (returns over lookback period)
def calculate_momentum(prices, lookback_period):
    returns = prices.pct_change(periods=lookback_period).iloc[-1]
    return returns


# Backtest the strategy
def backtest_momentum(tickers, lookback_period, holding_period, top_n, start_date, end_date):
    # Download data
    data = get_data(tickers, start_date, end_date)
    close_prices = pd.DataFrame({ticker: data[ticker]["Close"] for ticker in tickers})

    # Initialize portfolio variables
    portfolio_value = 10000  # Starting capital
    cash = portfolio_value
    positions = {}
    portfolio_history = []

    # Iterate through time (step by holding period)
    dates = close_prices.index[lookback_period:]  # Skip initial lookback period
    for i in range(0, len(dates) - holding_period, holding_period):
        current_date = dates[i]
        prices_window = close_prices.iloc[:i + lookback_period + 1]  # Up to current date

        # Calculate momentum for all tickers
        momentum = calculate_momentum(prices_window, lookback_period)
        momentum = momentum.dropna()

        # Select top performers
        top_performers = momentum.nlargest(top_n).index
        print(f"{current_date.date()}: Top performers - {top_performers.tolist()}")

        # Sell existing positions (end of holding period)
        if positions:
            for ticker in list(positions.keys()):
                sell_price = close_prices[ticker].iloc[i]
                cash += positions[ticker] * sell_price
                print(f"Sold {ticker} at {sell_price:.2f}")
                del positions[ticker]

        # Buy new positions
        investment_per_stock = cash / top_n
        for ticker in top_performers:
            buy_price = close_prices[ticker].iloc[i]
            shares = investment_per_stock / buy_price
            positions[ticker] = shares
            cash -= shares * buy_price
            print(f"Bought {shares:.2f} shares of {ticker} at {buy_price:.2f}")

        # Calculate portfolio value
        total_value = cash
        for ticker, shares in positions.items():
            total_value += shares * close_prices[ticker].iloc[i]
        portfolio_history.append(total_value)

    # Final liquidation
    final_date = dates[-1]
    for ticker in list(positions.keys()):
        sell_price = close_prices[ticker].iloc[-1]
        cash += positions[ticker] * sell_price
        print(f"Final sell {ticker} at {sell_price:.2f}")
        del positions[ticker]

    final_value = cash
    portfolio_history.append(final_value)

    return portfolio_history, dates[:len(portfolio_history)]


# Run the backtest
portfolio_history, dates = backtest_momentum(
    TICKERS, LOOKBACK_PERIOD, HOLDING_PERIOD, TOP_N, START_DATE, END_DATE
)

# Plot results
plt.figure(figsize=(10, 6))
plt.plot(dates, portfolio_history, label="Portfolio Value")
plt.title("Momentum Trading Strategy Backtest")
plt.xlabel("Date")
plt.ylabel("Portfolio Value ($)")
plt.legend()
plt.grid()
plt.show()

# Calculate performance metrics
initial_value = 10000
final_value = portfolio_history[-1]
total_return = (final_value - initial_value) / initial_value * 100
print(f"Initial Value: ${initial_value:.2f}")
print(f"Final Value: ${final_value:.2f}")
print(f"Total Return: {total_return:.2f}%")
