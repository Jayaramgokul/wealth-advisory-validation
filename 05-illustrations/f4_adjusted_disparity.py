"""F4. Raw and adjusted disparity, side by side.

Research: Barocas et al. (2021), conditional analysis in disaggregated evaluation.
Document: 03-research/fair-treatment.md

Question: two groups receive different risk scores. Is the gap explained by
legitimate suitability factors, or does it remain once they are accounted for?

    python 05-illustrations/f4_adjusted_disparity.py
"""

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


def scenario(explained: bool, seed: int = 0, n: int = 4000) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    group = rng.choice(["X", "Y"], n)
    # Group Y is older on average, a legitimate reason for a lower risk score.
    age = rng.normal(np.where(group == "Y", 55, 45), 10)
    tolerance = 80 - 0.6 * age + rng.normal(0, 8, n)
    score = tolerance + rng.normal(0, 5, n)
    if not explained:
        score = score - 4 * (group == "Y")            # an extra gap with no suitability reason
    return pd.DataFrame({"group": group, "age": age, "tolerance": tolerance, "score": score})


def main():
    for explained in (True, False):
        df = scenario(explained)
        raw = smf.ols("score ~ C(group)", df).fit()
        adj = smf.ols("score ~ C(group) + tolerance", df).fit()
        term = "C(group)[T.Y]"
        lo, hi = adj.conf_int().loc[term]
        print(f"\nScenario: {'gap explained by tolerance' if explained else 'gap partly unexplained'}")
        print(f"  raw gap (Y minus X):      {raw.params[term]:+.1f} points")
        print(f"  adjusted for tolerance:   {adj.params[term]:+.1f} points (95% CI {lo:+.1f} to {hi:+.1f}), "
              f"p = {adj.pvalues[term]:.2g}")
    print("\nWhat this shows: a raw gap alone cannot tell these two situations apart. Reporting the raw and\n"
          "adjusted figures together, with the control factors agreed in advance, separates a legitimate\n"
          "difference from one the model introduces.")


if __name__ == "__main__":
    main()
