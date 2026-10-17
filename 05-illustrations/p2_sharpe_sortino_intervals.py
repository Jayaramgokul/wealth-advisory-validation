"""P2. Risk-adjusted returns with intervals.

Research: Sharpe (1966, 1994); Sortino & Price (1994); Efron (1979).
Document: 03-research/portfolio-risk-and-performance.md

Question: if one portfolio is described as having better risk-adjusted
returns, is the difference real or noise?

    python 05-illustrations/p2_sharpe_sortino_intervals.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from common import (MODEL_PORTFOLIOS, TRADING_DAYS, block_bootstrap_index, market_returns,  # noqa: E402
                    portfolio_returns, save)

N_BOOT, BLOCK = 1000, 21


def sharpe(x):
    return x.mean() / x.std(ddof=1) * np.sqrt(TRADING_DAYS)


def sortino(x):
    downside = np.sqrt((np.minimum(x, 0) ** 2).mean())
    return x.mean() / downside * np.sqrt(TRADING_DAYS)


def main():
    rng = np.random.default_rng(0)
    m = market_returns()
    excess = {n: (portfolio_returns(m, n) - m["cash"]).to_numpy() for n in MODEL_PORTFOLIOS}
    # Resample whole blocks of days so that calm and crisis spells stay together.
    idx = block_bootstrap_index(len(m), BLOCK, N_BOOT, rng)
    boot = {n: np.array([sharpe(x[i]) for i in idx]) for n, x in excess.items()}

    print("Sharpe and Sortino ratios with 95% block-bootstrap intervals (simulated data)\n")
    for n, x in excess.items():
        so = np.array([sortino(x[i]) for i in idx[:300]])
        print(f"{n:12s} Sharpe {sharpe(x):5.2f} ({np.quantile(boot[n], .025):5.2f} to {np.quantile(boot[n], .975):5.2f})"
              f"   Sortino {sortino(x):5.2f} ({np.quantile(so, .025):5.2f} to {np.quantile(so, .975):5.2f})")

    diff = boot["85/15"] - boot["50/50"]
    lo, hi = np.quantile(diff, [0.025, 0.975])
    print(f"\n85/15 minus 50/50 Sharpe: {np.median(diff):+.3f} (95% interval {lo:+.3f} to {hi:+.3f})")
    if lo > 0 or hi < 0:
        ahead = "85/15" if lo > 0 else "50/50"
        verdict = f"The interval excludes zero: {ahead} has the better risk-adjusted return."
        if min(abs(lo), abs(hi)) < 0.02:
            verdict += " But only just: a slightly different history could reverse it, so treat the claim as fragile."
        else:
            verdict += " The claim is supported."
    else:
        verdict = "The interval includes zero: the data cannot tell these portfolios apart on risk-adjusted return."
    print(verdict)
    print("\nWhat this shows: point estimates of Sharpe and Sortino look precise but rest on a finite, dependent\n"
          "history. A performance claim in client material should survive its own interval; resampling\n"
          "blocks of days, not single days, respects the clustering of volatility.")

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.hist(diff, bins=40, color="#3182bd")
    ax.axvline(0, color="#d8543b")
    ax.set_xlabel("85/15 minus 50/50 Sharpe ratio (bootstrap)")
    ax.spines[["top", "right"]].set_visible(False)
    print(f"\nChart: {save(fig, 'p2_sharpe_difference')}")


if __name__ == "__main__":
    main()
