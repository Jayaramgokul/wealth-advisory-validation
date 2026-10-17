"""P1. Tail risk, three ways.

Research: Artzner et al. (1999); Rockafellar & Uryasev (2000).
Document: 03-research/portfolio-risk-and-performance.md

Question: does the loss a client is told to expect in a bad month hold up
when it is measured more than one way?

    python 05-illustrations/p1_tail_risk_three_ways.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from scipy import stats  # noqa: E402

from common import DISCLOSED_VOL, MODEL_PORTFOLIOS, market_returns, portfolio_returns, save  # noqa: E402

ALPHA, HORIZON, SIMS = 0.99, 21, 20_000


def tail_measures(daily, rng):
    monthly = daily.rolling(HORIZON).sum().dropna().to_numpy()
    # 1. Historical simulation: the actual worst months.
    h_var = -np.quantile(monthly, 1 - ALPHA)
    h_cvar = -monthly[monthly <= -h_var].mean()
    # 2. Parametric: assume monthly returns are normal.
    mu, sd = monthly.mean(), monthly.std(ddof=1)
    z = stats.norm.ppf(ALPHA)
    p_var = -(mu - z * sd)
    p_cvar = -(mu - sd * stats.norm.pdf(z) / (1 - ALPHA))
    # 3. Monte Carlo: build many months by resampling daily returns.
    paths = rng.choice(daily.to_numpy(), (SIMS, HORIZON)).sum(axis=1)
    m_var = -np.quantile(paths, 1 - ALPHA)
    m_cvar = -paths[paths <= -m_var].mean()
    return {"historical": (h_var, h_cvar), "parametric": (p_var, p_cvar), "monte carlo": (m_var, m_cvar)}


def main():
    rng = np.random.default_rng(0)
    m = market_returns()
    rows = {}
    print(f"One-month {ALPHA:.0%} tail loss, three ways (simulated data)\n")
    print(f"{'portfolio':12s} {'method':12s} {'VaR':>7s} {'CVaR':>7s}")
    for name in MODEL_PORTFOLIOS:
        res = tail_measures(portfolio_returns(m, name), rng)
        rows[name] = res
        for method, (v, c) in res.items():
            print(f"{name:12s} {method:12s} {v:7.1%} {c:7.1%}")
        implied = stats.norm.ppf(ALPHA) * DISCLOSED_VOL[name] / np.sqrt(12)
        worst = max(c for _, c in res.values())
        print(f"{'':12s} {'band implies':12s} {implied:7.1%}   worst CVaR is {worst / implied:.1f}x that\n")

    print("What this shows: the normal model gives the smallest tail loss for every portfolio, because\n"
          "real returns have fat tails. CVaR, the average loss beyond VaR, is what Artzner et al. call a\n"
          "coherent measure; VaR alone says nothing about how bad the worst months are. If the methods\n"
          "disagree this much, a disclosed risk band built on the normal model is not reliable.")

    fig, ax = plt.subplots(figsize=(7, 3.2))
    x = np.arange(len(rows))
    for i, method in enumerate(["parametric", "historical", "monte carlo"]):
        ax.bar(x + (i - 1) * 0.25, [rows[n][method][1] for n in rows], 0.25, label=method)
    ax.set_xticks(x, list(rows))
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    ax.set_ylabel("One-month 99% CVaR")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    print(f"\nChart: {save(fig, 'p1_tail_risk')}")


if __name__ == "__main__":
    main()
