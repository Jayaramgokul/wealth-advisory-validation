"""C1. Proprietary product tilt.

Research: SEC order against SoFi Wealth (2021, Release IA-5826); duty of loyalty (IA-5248).
Document: 03-research/conflicts-of-interest.md

Question: for each sleeve of a portfolio the model chooses between an
own-brand fund and comparable third-party funds. Is the own-brand fund chosen
more often than a product-neutral rule would choose it, and what does that
cost clients?

    python 05-illustrations/c1_proprietary_product_tilt.py
"""

import numpy as np
import pandas as pd
from scipy import stats

from common import wilson

IN_HOUSE_FEE, PEER_FEE = 0.0045, 0.0010     # annual expense ratios
NEUTRAL_SHARE = 0.10                        # how often a cost-and-mandate ranking picks the own-brand fund
SLEEVE = 0.40                               # share of the account in the sleeve where the choice is made


def main():
    rng = np.random.default_rng(0)
    n = 8000
    size = rng.choice(["smaller", "mid-size", "largest"], n, p=[0.5, 0.35, 0.15])
    balance = np.select([size == "smaller", size == "mid-size"],
                        [rng.uniform(1e3, 25e3, n), rng.uniform(25e3, 1e5, n)], rng.uniform(1e5, 1e6, n))
    tilt = pd.Series(size).map({"smaller": 0.10, "mid-size": 0.12, "largest": 0.55}).to_numpy()
    in_house = rng.random(n) < tilt
    print(f"Share of sleeves in the own-brand fund, against a product-neutral benchmark of {NEUTRAL_SHARE:.0%}\n")
    for seg in ["smaller", "mid-size", "largest"]:
        m = size == seg
        k, total = int(in_house[m].sum()), int(m.sum())
        lo, hi = wilson(k, total)
        p = stats.binomtest(k, total, NEUTRAL_SHARE, alternative="greater").pvalue
        excess = (k / total - NEUTRAL_SHARE) * balance[m].sum() / total * SLEEVE * (IN_HOUSE_FEE - PEER_FEE)
        print(f"{seg + " accounts":17s} {k / total:5.0%} (95% CI {lo:.0%} to {hi:.0%})   p = {p:.2g}   "
              f"extra fees about ${excess:,.0f} per client per year")
    print("\nWhat this shows: a conflict in automated advice can live in one rule that applies only to\n"
          "some clients, so the overall share can look modest. Compare with a neutral benchmark segment\n"
          "by segment, put a cost on the difference, and check that the disclosure is specific enough for\n"
          "a client to understand it, not merely that a conflict is mentioned.")


if __name__ == "__main__":
    main()
