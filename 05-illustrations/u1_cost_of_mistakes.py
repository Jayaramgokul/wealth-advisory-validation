"""U1. Asymmetric cost of mistakes.

Research: Bishop (2006), Pattern Recognition and Machine Learning, section 1.5 (decision theory).
Document: 03-research/decisions-under-uncertainty.md

Question: model A is more accurate than model B. Is it better for clients,
when putting someone in a riskier portfolio than they can bear is worse than
putting them in a safer one?

    python 05-illustrations/u1_cost_of_mistakes.py
"""

import numpy as np

from common import BUCKETS, bucket, questionnaire

# Illustrative cost matrix: cost[placed, true]. Too aggressive costs three times as much per step.
K = len(BUCKETS)
COST = np.array([[3 * (p - t) if p > t else (t - p) for t in range(K)] for p in range(K)], float)


def main():
    rng = np.random.default_rng(0)
    clients = questionnaire(n=6000)
    true = bucket(clients["true_tolerance"])
    noise = rng.normal(0, 7, len(clients))
    models = {"model A": bucket(clients["true_tolerance"] + noise + 3),     # errs towards too aggressive
              "model B": bucket(clients["true_tolerance"] + noise - 3)}     # errs towards too cautious
    print("Cost matrix (rows: placed, columns: true bucket), agreed with the business in advance:\n")
    print(COST.astype(int))
    print()
    for name, placed in models.items():
        acc = np.mean(placed == true)
        over, under = np.mean(placed > true), np.mean(placed < true)
        cost = COST[placed, true].mean()
        print(f"{name}: accuracy {acc:.0%}   too aggressive {over:.0%}   too cautious {under:.0%}   "
              f"expected cost {cost:.2f} per client")
    print("\nWhat this shows: accuracy treats every mistake alike, so it prefers the model that harms clients\n"
          "more. Expected cost under an agreed cost matrix ranks them the other way. The matrix is a\n"
          "business and compliance decision, written down before testing; the validator's job is to make\n"
          "it explicit and report against it.")


if __name__ == "__main__":
    main()
