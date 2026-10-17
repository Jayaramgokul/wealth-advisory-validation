"""P5. Confidence intervals on risk metrics.

Research: Efron (1979); Hastie, Tibshirani & Friedman (2009).
Document: 03-research/portfolio-risk-and-performance.md

Question: a portfolio is disclosed as having volatility within a band. Is
that still true at the upper end of what the data supports?

    python 05-illustrations/p5_intervals_on_risk_metrics.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from common import (DISCLOSED_VOL, MODEL_PORTFOLIOS, TRADING_DAYS, block_bootstrap_index,  # noqa: E402
                    market_returns, portfolio_returns, save)


def main():
    rng = np.random.default_rng(0)
    m = market_returns()
    idx = block_bootstrap_index(len(m), 21, 1000, rng)
    rows = []
    print("Annual volatility with 95% block-bootstrap intervals, against the disclosed band (simulated data)\n")
    for name in MODEL_PORTFOLIOS:
        r = portfolio_returns(m, name).to_numpy()
        vols = r[idx].std(axis=1, ddof=1) * np.sqrt(TRADING_DAYS)
        point, lo, hi = r.std(ddof=1) * np.sqrt(TRADING_DAYS), *np.quantile(vols, [0.025, 0.975])
        band = DISCLOSED_VOL[name]
        verdict = "inside the band" if hi <= band else ("point estimate inside, upper end outside" if point <= band
                                                         else "outside the band")
        rows.append((name, point, lo, hi, band))
        print(f"{name:12s} {point:5.1%} ({lo:5.1%} to {hi:5.1%})   disclosed {band:4.0%}   {verdict}")
    print("\nWhat this shows: a single volatility figure hides how much it could plausibly be. Testing the\n"
          "upper end of the interval against the disclosed band is the honest check; where it fails, the\n"
          "band should be widened or the portfolio de-risked.")

    fig, ax = plt.subplots(figsize=(6, 2.8))
    for i, (name, point, lo, hi, band) in enumerate(rows):
        ax.errorbar(point, i, xerr=[[point - lo], [hi - point]], fmt="o", color="#3182bd", capsize=3)
        ax.plot([band, band], [i - 0.3, i + 0.3], color="#d8543b", lw=2)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows])
    ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    ax.set_xlabel("Annual volatility (95% interval); red = disclosed band")
    ax.spines[["top", "right"]].set_visible(False)
    print(f"\nChart: {save(fig, 'p5_volatility_intervals')}")


if __name__ == "__main__":
    main()
