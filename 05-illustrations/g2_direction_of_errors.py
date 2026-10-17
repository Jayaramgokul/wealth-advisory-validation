"""G2. Direction of errors by group.

Research: Buolamwini & Gebru (2018); Barocas et al. (2021).
Document: 03-research/groups-an-average-hides.md

Question: two client groups are misplaced equally often. Do their mistakes
lean the same way?

    python 05-illustrations/g2_direction_of_errors.py
"""

import numpy as np
from scipy import stats

from common import bucket, questionnaire, wilson


def main():
    rng = np.random.default_rng(0)
    clients = questionnaire(n=6000)
    true = bucket(clients["true_tolerance"])
    # A placement model whose error leans differently by region (for example, a regional input
    # that proxies for something the model should not use).
    lean = clients["region"].map({"north": 4, "south": -4, "east": 0, "west": 0}).to_numpy()
    placed = bucket(clients["true_tolerance"] + rng.normal(0, 6, len(clients)) + lean)
    print(f"{'region':8s} {'misplaced':>10s} {'too aggressive (95% CI)':>26s} {'too cautious (95% CI)':>24s}")
    counts = {}
    for region in sorted(clients["region"].unique()):
        m = (clients["region"] == region).to_numpy()
        n = int(m.sum())
        over, under = int((placed[m] > true[m]).sum()), int((placed[m] < true[m]).sum())
        counts[region] = (over, under, n)
        lo_o, hi_o = wilson(over, n)
        lo_u, hi_u = wilson(under, n)
        print(f"{region:8s} {(over + under) / n:10.0%} {over / n:9.0%} ({lo_o:.0%} to {hi_o:.0%})       "
              f"{under / n:7.0%} ({lo_u:.0%} to {hi_u:.0%})")
    table = [[o, u] for o, u, _ in counts.values()]
    print(f"\nDo errors lean differently across regions? chi-square p = {stats.chi2_contingency(table)[1]:.2g}")
    print("\nWhat this shows: north and south are misplaced about as often as each other, so an error-rate\n"
          "check passes them both. But north's clients are pushed into too much risk and south's into too\n"
          "little: different harms, needing different fixes. Report the direction, not just the rate.")


if __name__ == "__main__":
    main()
