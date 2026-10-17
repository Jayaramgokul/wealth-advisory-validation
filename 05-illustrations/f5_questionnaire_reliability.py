"""F5. Does the risk questionnaire measure every client equally well?

Research: Grable & Lytton (1999); Barocas et al. (2021), measurement validity.
Document: 03-research/fair-treatment.md

Question: the risk score is a measurement. Is it as reliable for novice
investors as for experienced ones?

    python 05-illustrations/f5_questionnaire_reliability.py
"""

import numpy as np

from common import cronbach_alpha, questionnaire

QUESTIONS = [f"q{i}" for i in range(1, 9)]


def main():
    rng = np.random.default_rng(0)
    df = questionnaire()
    print("Internal consistency of the 8-item questionnaire (Cronbach's alpha), simulated answers\n")
    for group, part in df.groupby("experience"):
        items = part[QUESTIONS]
        a = cronbach_alpha(items)
        boot = [cronbach_alpha(items.iloc[rng.integers(0, len(items), len(items))]) for _ in range(300)]
        lo, hi = np.quantile(boot, [0.025, 0.975])
        corr = np.corrcoef(items.mean(axis=1), part["true_tolerance"])[0, 1]
        print(f"{group:12s} alpha {a:.2f} (95% CI {lo:.2f} to {hi:.2f})   "
              f"correlation of score with true tolerance {corr:.2f}")
    print("\nWhat this shows: the same questions can measure some clients well and others poorly. Lower\n"
          "reliability means more misplacements for that group, and it weakens every fairness test that\n"
          "uses the score as its yardstick. Remedies include clearer items, follow-up questions when answers\n"
          "contradict, or disclosing the limitation.")


if __name__ == "__main__":
    main()
