"""R1. Dependent data.

Research: Saria & Subbaswamy (2019); Kunsch (1989), the block bootstrap.
Document: 03-research/shift-and-dependence.md

Question: a 95% interval on a portfolio's volatility is computed from five
years of daily returns. Bad days cluster together. Does the interval contain
the true volatility 95% of the time?

    python 05-illustrations/r1_dependent_data.py
"""

import numpy as np

from common import TRADING_DAYS, block_bootstrap_index, market_returns, portfolio_returns

HISTORIES, YEARS, RESAMPLES, BLOCK = 200, 5, 300, 63


def main():
    rng = np.random.default_rng(0)
    truth = portfolio_returns(market_returns(years=200, seed=999), "50/50").std() * np.sqrt(TRADING_DAYS)
    T = YEARS * TRADING_DAYS
    covered = {"days resampled one at a time": [], f"blocks of {BLOCK} days": []}
    width = {k: [] for k in covered}
    for h in range(HISTORIES):
        r = portfolio_returns(market_returns(years=YEARS, seed=1000 + h), "50/50").to_numpy()
        for label, idx in (("days resampled one at a time", rng.integers(0, T, (RESAMPLES, T))),
                           (f"blocks of {BLOCK} days", block_bootstrap_index(T, BLOCK, RESAMPLES, rng))):
            vols = r[idx].std(axis=1, ddof=1) * np.sqrt(TRADING_DAYS)
            lo, hi = np.quantile(vols, [0.025, 0.975])
            covered[label].append(lo <= truth <= hi)
            width[label].append(hi - lo)
    print(f"True long-run volatility of the 50/50 portfolio: {truth:.1%}")
    print(f"{HISTORIES} independent {YEARS}-year histories, a 95% bootstrap interval from each (simulated)\n")
    for label in covered:
        print(f"{label:30s} contains the truth {np.mean(covered[label]):4.0%} of the time, "
              f"average width {np.mean(width[label]):.1%}")
    print("\nWhat this shows: resampling single days assumes they are independent. When bad days cluster,\n"
          "that gives intervals that are too narrow and miss the truth far more than 5% of the time.\n"
          "Resampling blocks keeps the clustering and brings coverage closer to what was promised.")
    if np.mean(covered[f"blocks of {BLOCK} days"]) < 0.90:
        print("Even blocks fall short here: five years may hold no crisis, or one long one, and no resampling\n"
              "scheme can recover what the history does not contain. Short histories need wider bands or\n"
              "longer data, and the limitation should be stated beside the interval.")


if __name__ == "__main__":
    main()
