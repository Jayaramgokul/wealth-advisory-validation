"""P3. Volatility estimator sensitivity.

Research: J.P. Morgan/Reuters (1996), RiskMetrics Technical Document.
Document: 03-research/portfolio-risk-and-performance.md

Question: does the choice between an exponentially weighted (EWMA, lambda
0.94) and an equally weighted sample estimate of volatility change what the
client experiences?

    python 05-illustrations/p3_ewma_vs_sample_volatility.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from common import DISCLOSED_VOL, TRADING_DAYS, market_returns, portfolio_returns, save  # noqa: E402

LAMBDA, WINDOW = 0.94, 252
# Materiality, set before looking at results: 2 points more days in breach, or 0.10 in the risk scale.
MATERIAL_BREACH, MATERIAL_SCALE = 0.02, 0.10


def ewma_vol(r, lam=LAMBDA):
    var = np.empty(len(r))
    var[0] = r[:20].var()
    for t in range(1, len(r)):
        var[t] = lam * var[t - 1] + (1 - lam) * r[t - 1] ** 2
    return np.sqrt(var * TRADING_DAYS)


def main():
    m = market_returns()
    r = portfolio_returns(m, "50/50")
    sample = r.rolling(WINDOW).std(ddof=1).shift(1) * np.sqrt(TRADING_DAYS)
    ewma = ewma_vol(r.to_numpy())
    realised = r.rolling(21).std(ddof=1).shift(-20) * np.sqrt(TRADING_DAYS)
    d = (np.vstack([sample, ewma, realised]).T)
    ok = ~np.isnan(d).any(axis=1)
    sample, ewma, realised = d[ok, 0], d[ok, 1], d[ok, 2]

    target = DISCLOSED_VOL["50/50"]
    print("Volatility targeting the 50/50 portfolio to its disclosed band (simulated data)\n")
    results = {}
    for name, f in (("sample (1 year)", sample), ("EWMA (0.94)", ewma)):
        scale = np.minimum(1.5, target / f)
        held = realised * scale
        results[name] = {"error": np.abs(f - realised).mean(), "breach": (held > 1.25 * target).mean(),
                         "scale": scale.mean()}
        print(f"{name:16s} forecast error {results[name]['error']:.1%}   days above 1.25x band "
              f"{results[name]['breach']:.1%}   average risk scale {scale.mean():.2f}")
    a, b = results.values()
    gap_breach, gap_scale = abs(a["breach"] - b["breach"]), abs(a["scale"] - b["scale"])
    print(f"\nDifference between estimators: {gap_breach:.1%} of days in breach, {gap_scale:.2f} in risk scale.")
    if gap_breach > MATERIAL_BREACH or gap_scale > MATERIAL_SCALE:
        print("The choice is material here: it changes exposures or breaches, so it needs a documented rationale.")
    else:
        print("Outcomes are robust to the estimator choice in this data; record the test so the choice is evidenced.")
    print("\nWhat this shows: EWMA reacts faster to a crisis, while a one-year window remembers calm periods.\n"
          "Whether that difference matters for clients is an empirical question, and this is how to answer it.")

    fig, ax = plt.subplots(figsize=(7, 3))
    t = np.arange(len(realised))[-1500:]
    ax.plot(t, realised[-1500:], color="#bbb", lw=0.8, label="realised next month")
    ax.plot(t, sample[-1500:], label="sample, 1 year")
    ax.plot(t, ewma[-1500:], label="EWMA 0.94")
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    ax.set_ylabel("Annualised volatility")
    ax.legend(frameon=False, fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    print(f"\nChart: {save(fig, 'p3_volatility_estimators')}")


if __name__ == "__main__":
    main()
