import datetime as dt
from dataclasses import dataclass
from typing import List

import pandas as pd
import yfinance as yf

@dataclass
class Trade:
    date: dt.date
    shares: float
    price: float
    cost: float

@dataclass
class BacktestResult:
    ticker: str
    strategy: str
    total_invested: float
    final_value: float


def download_prices(ticker: str, start: str, end: str) -> pd.Series:
    """Download adjusted close prices from Yahoo Finance."""
    data = yf.download(ticker, start=start, end=end, progress=False)
    return data["Adj Close"].dropna()


def dca_strategy(prices: pd.Series, amount: float) -> List[Trade]:
    """Invest a fixed amount on the first trading day of each month."""
    trades = []
    monthly = prices.resample("M").first()
    for date, price in monthly.items():
        shares = amount / price
        trades.append(Trade(date=date.date(), shares=shares, price=price, cost=amount))
    return trades


def dip_buy_strategy(prices: pd.Series, amount: float) -> List[Trade]:
    """Invest double when the previous month's return is negative."""
    trades = []
    monthly = prices.resample("M").first()
    prev_price = None
    for date, price in monthly.items():
        invest_amount = amount
        if prev_price is not None and price < prev_price:
            invest_amount = amount * 2
        shares = invest_amount / price
        trades.append(Trade(date=date.date(), shares=shares, price=price, cost=invest_amount))
        prev_price = price
    return trades


STRATEGIES = {
    "DCA": dca_strategy,
    "DipBuy": dip_buy_strategy,
}


def run_backtest(ticker: str, strategy_name: str, amount: float, start: str, end: str) -> BacktestResult:
    prices = download_prices(ticker, start, end)
    strategy = STRATEGIES[strategy_name]
    trades = strategy(prices, amount)
    total_shares = sum(t.shares for t in trades)
    total_invested = sum(t.cost for t in trades)
    final_price = prices.iloc[-1]
    final_value = total_shares * final_price
    return BacktestResult(ticker, strategy_name, total_invested, final_value)


def main():
    tickers = ["QQQ", "VOO"]
    start = "2015-01-01"
    end = dt.date.today().strftime("%Y-%m-%d")
    amount = 1000  # invest per month

    results = []
    for ticker in tickers:
        for strategy in STRATEGIES.keys():
            res = run_backtest(ticker, strategy, amount, start, end)
            results.append(res)

    for r in results:
        gain = r.final_value - r.total_invested
        print(f"{r.ticker} {r.strategy}: invested ${r.total_invested:.2f}, final ${r.final_value:.2f}, gain ${gain:.2f}")


if __name__ == "__main__":
    main()
