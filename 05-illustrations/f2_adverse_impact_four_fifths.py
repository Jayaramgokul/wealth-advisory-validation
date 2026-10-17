"""F2. Adverse impact with honest statistics.

Research: EEOC Uniform Guidelines (1978), the four-fifths rule; Barocas et al. (2021).
Document: 03-research/fair-treatment.md

Question: does any group receive a favourable outcome (here, access to growth
portfolios) at less than four-fifths the rate of the best-treated group, and
is each group large enough for the test to mean anything?

    python 05-illustrations/f2_adverse_impact_four_fifths.py
"""

import numpy as np
import pandas as pd
from scipy import stats

from common import smallest_detectable_gap, wilson


def adverse_impact(df, group="group", outcome="favourable"):
    rows = []
    for g, part in df.groupby(group):
        k, n = int(part[outcome].sum()), len(part)
        lo, hi = wilson(k, n)
        rows.append({"group": g, "clients": n, "rate": k / n, "ci_low": lo, "ci_high": hi})
    t = pd.DataFrame(rows)
    t["impact_ratio"] = t["rate"] / t["rate"].max()
    p_all = df[outcome].mean()
    t["smallest_detectable_gap"] = [smallest_detectable_gap(p_all, n, len(df) - n) for n in t["clients"]]
    chi2, p, _, _ = stats.chi2_contingency(pd.crosstab(df[group], df[outcome]))
    return t, p


def main():
    rng = np.random.default_rng(0)
    # Simulated outcomes: groups A-C similar, D genuinely lower, E very small.
    spec = {"A": (2000, 0.50), "B": (1800, 0.49), "C": (1500, 0.51), "D": (1400, 0.37), "E": (60, 0.42)}
    df = pd.concat([pd.DataFrame({"group": g, "favourable": rng.random(n) < p}) for g, (n, p) in spec.items()],
                   ignore_index=True)
    t, p = adverse_impact(df)
    pd.set_option("display.width", 120)
    print(t.to_string(index=False, float_format=lambda v: f"{v:.3f}"))
    print(f"\nChi-square test of equal rates: p = {p:.2g}")
    for _, r in t.iterrows():
        if r["impact_ratio"] < 0.8:
            print(f"Group {r['group']}: impact ratio {r['impact_ratio']:.2f}, below four-fifths.")
        if r["smallest_detectable_gap"] > 0.10:
            print(f"Group {r['group']}: only {int(r['clients'])} clients, so a gap as large as "
                  f"{r['smallest_detectable_gap']:.0%} could go undetected. Report as inconclusive, not as passing.")
    print("\nWhat this shows: the four-fifths rule is a screen, not a verdict. Pair it with a significance\n"
          "test and intervals, and state the power: a small group that 'passes' may simply be too small to\n"
          "fail.")


if __name__ == "__main__":
    main()
