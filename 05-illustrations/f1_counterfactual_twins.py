"""F1. Counterfactual twin clients.

Research: Kusner et al. (2017), Counterfactual Fairness.
Document: 03-research/fair-treatment.md

Question: if we change only one attribute of a client (region, sex), keeping
every questionnaire answer the same, does the recommendation change?

The test treats the scoring model as a black box. Two minimal stand-ins are
defined below so the method can be seen working: one uses only the answers,
the other quietly adds a regional adjustment.

    python 05-illustrations/f1_counterfactual_twins.py
"""

import numpy as np  # noqa: E402

from common import questionnaire, wilson  # noqa: E402

CUTOFFS = [30, 45, 60, 75]                      # score -> one of five risk buckets
QUESTIONS = [f"q{i}" for i in range(1, 9)]


def score_answers_only(c):
    return (c[QUESTIONS].to_numpy() - 1).mean(axis=1) / 4 * 100


def score_with_region(c):
    adjustment = c["region"].map({"north": 0, "south": -4, "east": 0, "west": 3}).to_numpy()
    return np.clip(score_answers_only(c) + adjustment, 0, 100)


def bucket(scores):
    return np.searchsorted(CUTOFFS, scores, side="right")


def twin_test(model, clients, attribute):
    base = bucket(model(clients))
    rows = []
    for value in sorted(clients[attribute].unique()):
        twins = clients.copy()
        twins[attribute] = value
        changed = (bucket(model(twins)) != base)[(clients[attribute] != value).to_numpy()]
        k, n = int(changed.sum()), len(changed)
        rows.append((value, k / n, *wilson(k, n)))
    return rows


def main():
    clients = questionnaire()
    for label, model in (("answers only", score_answers_only), ("answers + regional adjustment", score_with_region)):
        print(f"\nModel under review: {label}")
        for attribute in ("sex", "region"):
            for value, rate, lo, hi in twin_test(model, clients, attribute):
                print(f"  set {attribute:6s} to {value:7s}: recommendation changes for {rate:5.1%} of clients "
                      f"(95% CI {lo:.1%} to {hi:.1%})")
    print("\nWhat this shows: the twin test needs no knowledge of the model's internals. With identical\n"
          "answers, nothing should move. Any change is a direct effect of the attribute, which is either\n"
          "a documented suitability factor or a fairness finding. Attributes that are proxies for protected\n"
          "characteristics, like region, deserve the same test as the characteristics themselves.")


if __name__ == "__main__":
    main()
