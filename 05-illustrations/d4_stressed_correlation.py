"""D4. Correlation breakdown under stress.

Research: Gebru et al. (2021) (does the data contain the conditions that matter?).
Document: 03-research/data-fitness.md

Question: in the crises in the data, bonds rallied and cushioned equity
losses. How much worse would a crisis be for each portfolio if that
relationship failed, as it did in 2022 when stocks and bonds fell together?

    python 05-illustrations/d4_stressed_correlation.py
"""

import numpy as np

from common import ASSETS, MODEL_PORTFOLIOS, TRADING_DAYS, market_returns

STRESSED_EQUITY_BOND = 0.5


def vol(weights, cov):
    w = np.asarray(weights)
    return float(np.sqrt(w @ cov @ w))


def main():
    m = market_returns()
    calm = m.loc[m["regime"] == "calm", ASSETS]
    crisis = m.loc[m["regime"] == "crisis", ASSETS]
    cov_crisis = crisis.cov().to_numpy() * TRADING_DAYS
    sd = np.sqrt(np.diag(cov_crisis))
    corr = crisis.corr().to_numpy().copy()
    corr[0, 1] = corr[1, 0] = STRESSED_EQUITY_BOND
    cov_stress = np.outer(sd, sd) * corr

    print(f"Equity-bond correlation: calm {calm.corr().iloc[0, 1]:+.2f}, crises in the data "
          f"{crisis.corr().iloc[0, 1]:+.2f}, hypothetical {STRESSED_EQUITY_BOND:+.2f}\n")
    print("Annualised volatility during a crisis (simulated data)\n")
    print(f"{'portfolio':12s} {'as in the data':>15s} {'hedge fails':>12s} {'increase':>9s}")
    for name, w in MODEL_PORTFOLIOS.items():
        a, b = vol(w, cov_crisis), vol(w, cov_stress)
        print(f"{name:12s} {a:15.1%} {b:12.1%} {b / a - 1:9.0%}")
    print("\nWhat this shows: the history only contains the crises it happened to contain. The portfolio\n"
          "that leans most on bonds, the 20/80, depends most on bonds behaving as they did, and\n"
          "is the one whose clients are least able to absorb the surprise. A validation should stress\n"
          "the relationships each portfolio relies on, not only replay the past.")


if __name__ == "__main__":
    main()
