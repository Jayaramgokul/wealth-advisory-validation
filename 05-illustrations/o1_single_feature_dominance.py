"""O1. Single-feature dominance.

Research: WEF, IMDA & PDPC (2020), Companion to the Model AI Governance Framework (robustness).
Document: 03-research/operation.md

Question: the risk score combines eight questionnaire answers and the
client's age. If one input were neutralised (set to its typical value), how
many recommendations would change?

    python 05-illustrations/o1_single_feature_dominance.py
"""

import numpy as np

from common import QUESTIONS, bucket, questionnaire

AGREED_SHARE = 0.30        # no single input should move more than this share of recommendations

# A stand-in scoring rule: question 1 ("what would you do after a 20% fall?") is heavily weighted.
WEIGHTS = {"q1": 0.45, **{q: 0.05 for q in QUESTIONS[1:]}, "age": 0.20}


def score(c):
    parts = {q: (c[q].to_numpy() - 1) / 4 * 100 for q in QUESTIONS}
    parts["age"] = np.clip((85 - c["age"].to_numpy()) / 64 * 100, 0, 100)
    return sum(WEIGHTS[k] * parts[k] for k in WEIGHTS)


def main():
    clients = questionnaire(n=6000)
    base = bucket(score(clients))
    print("Share of recommendations that change when one input is set to its median (simulated)\n")
    for k in sorted(WEIGHTS, key=WEIGHTS.get, reverse=True):
        neutral = clients.copy()
        neutral[k] = clients[k].median()
        changed = np.mean(bucket(score(neutral)) != base)
        flag = "   dominates" if changed > AGREED_SHARE else ""
        print(f"{k:4s} weight {WEIGHTS[k]:.2f}   changes {changed:5.1%}{flag}")
    print("\nWhat this shows: if one answer moves a large share of recommendations, a misread question, a\n"
          "form bug or a bad data feed for that field changes the advice for many clients at once. Measured\n"
          "influence, not stated weight, is what the agreed limit should apply to.")


if __name__ == "__main__":
    main()
