"""D2. Look-ahead bias.

Research: Gebru et al. (2021), Datasheets for Datasets (when was each field known?).
Document: 03-research/data-fitness.md

Question: a simple rule moves the 50/50 portfolio into cash when recent
equity returns are negative. Does its backtest use only information that was
available at the time of each decision?

    python 05-illustrations/d2_look_ahead_bias.py
"""

import numpy as np

from common import market_returns, portfolio_returns


def sharpe(x):
    return x.mean() / x.std(ddof=1) * np.sqrt(12)


def main():
    m = market_returns(years=20)
    monthly_eq = (1 + m["equity"]).groupby(m.index.to_period("M")).prod() - 1
    monthly_pf = (1 + portfolio_returns(m, "50/50")).groupby(m.index.to_period("M")).prod() - 1
    monthly_cash = (1 + m["cash"]).groupby(m.index.to_period("M")).prod() - 1
    trend = monthly_eq.rolling(3).sum()

    def backtest(signal):
        invested = (signal > 0).to_numpy()
        return np.where(invested, monthly_pf, monthly_cash)[3:]

    leaky = backtest(trend)               # this month's decision uses this month's return: not yet known
    honest = backtest(trend.shift(1))     # decision uses returns up to last month only
    hold = monthly_pf.to_numpy()[3:]
    print("Monthly timing rule on the 50/50 portfolio, 20 years of simulated data\n")
    for name, x in (("buy and hold", hold), ("rule, with look-ahead", leaky), ("rule, point-in-time", honest)):
        print(f"{name:24s} annual return {(np.prod(1 + x)) ** (12 / len(x)) - 1:6.2%}   Sharpe {sharpe(x):5.2f}")
    print("\nWhat this shows: one misaligned month turns an ordinary rule into an apparently brilliant one.\n"
          "The fix is a record of when each field became known, and a backtest that respects it. Any\n"
          "result that shrinks sharply once fields are lagged was never available to a client.")


if __name__ == "__main__":
    main()
