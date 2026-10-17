"""F3. Intersectional groups, with the worst group as co-headline.

Research: Buolamwini & Gebru (2018), Gender Shades; Barocas et al. (2021).
Document: 03-research/fair-treatment.md

Question: the overall suitability rate looks fine. Is there a combination of
client characteristics that is badly served, which no single-factor check
would reveal?

    python 05-illustrations/f3_worst_group_intersectional.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

from common import bh, save, wilson  # noqa: E402

MIN_CELL = 80


def main():
    rng = np.random.default_rng(0)
    n = 6000
    df = pd.DataFrame({"age_band": rng.choice(["under 40", "40-64", "65+"], n, p=[.4, .4, .2]),
                       "experience": rng.choice(["novice", "experienced"], n, p=[.4, .6]),
                       "account": rng.choice(["small", "large"], n, p=[.6, .4])})
    # Simulated suitability: each factor alone costs little, but older novices are poorly served.
    p = 0.82 - 0.03 * (df["age_band"] == "65+") - 0.03 * (df["experience"] == "novice") \
        - 0.15 * ((df["age_band"] == "65+") & (df["experience"] == "novice"))
    df["suitable"] = rng.random(n) < p

    print("Single factors (what a one-axis check sees):")
    for f in ["age_band", "experience", "account"]:
        print("  " + ", ".join(f"{k}: {v:.0%}" for k, v in df.groupby(f)["suitable"].mean().items()))

    cells = df.groupby(["age_band", "experience", "account"])["suitable"].agg(["sum", "count"]).reset_index()
    cells["rate"] = cells["sum"] / cells["count"]
    cells[["lo", "hi"]] = [wilson(int(s), int(c)) for s, c in zip(cells["sum"], cells["count"])]
    total_ok, total = int(df["suitable"].sum()), len(df)
    cells["p"] = [stats.fisher_exact([[s, c - s], [total_ok - s, total - total_ok - (c - s)]])[1]
                  for s, c in zip(cells["sum"], cells["count"])]
    cells["q"] = bh(cells["p"])
    cells["too_small"] = cells["count"] < MIN_CELL
    worst = cells[~cells["too_small"]].sort_values("rate").iloc[0]
    print(f"\nOverall suitable: {df['suitable'].mean():.0%}")
    print(f"Worst group: {worst['age_band']}, {worst['experience']}, {worst['account']} account: {worst['rate']:.0%} "
          f"(95% CI {worst['lo']:.0%} to {worst['hi']:.0%}; corrected q = {worst['q']:.2g})")
    if cells["too_small"].any():
        print(f"{int(cells['too_small'].sum())} cell(s) below {MIN_CELL} clients are listed as too small to judge.")
    print("\nWhat this shows: each factor on its own costs a few points, but one combination is far worse.\n"
          "Report the worst group beside every average, with its interval, and correct for having looked at\n"
          "many groups.")

    cells = cells.sort_values("rate")
    fig, ax = plt.subplots(figsize=(6.5, 4))
    y = np.arange(len(cells))
    ax.errorbar(cells["rate"], y, xerr=[cells["rate"] - cells["lo"], cells["hi"] - cells["rate"]], fmt="o",
                capsize=2, color="#3182bd")
    ax.axvline(df["suitable"].mean(), color="#888", ls="--", lw=1)
    ax.set_yticks(y, cells["age_band"] + " · " + cells["experience"] + " · " + cells["account"], fontsize=7)
    ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    ax.set_xlabel("Suitably placed (95% CI); dashed = overall")
    ax.spines[["top", "right"]].set_visible(False)
    print(f"\nChart: {save(fig, 'f3_intersectional')}")


if __name__ == "__main__":
    main()
