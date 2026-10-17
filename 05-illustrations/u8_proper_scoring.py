"""U8. Proper scoring rules.

Research: Gneiting & Raftery (2007); Brier (1950); Bishop (2006), section 1.5.
Document: 03-research/decisions-under-uncertainty.md

Question: a model estimates the probability that a client will sell in a
downturn. Two versions rank clients identically, so their accuracy is the
same. Is one of them more honest about its uncertainty?

    python 05-illustrations/u8_proper_scoring.py
"""

import numpy as np


def sharpen(p, power):
    """Push probabilities towards 0 or 1 without changing their order."""
    return p ** power / (p ** power + (1 - p) ** power)


def main():
    rng = np.random.default_rng(0)
    n = 20000
    true_p = 1 / (1 + np.exp(-rng.normal(-0.5, 1.2, n)))
    y = rng.random(n) < true_p
    models = {"calibrated": true_p, "overconfident": sharpen(true_p, 3)}
    print("Two probability models for 'client sells in a downturn' (simulated)\n")
    for name, p in models.items():
        acc = np.mean((p > 0.5) == y)
        brier = np.mean((p - y) ** 2)
        logloss = -np.mean(np.where(y, np.log(p), np.log(1 - p)))
        high = p > 0.9
        print(f"{name:14s} accuracy {acc:.1%}   Brier {brier:.3f}   log loss {logloss:.3f}   "
              f"says >90%: {high.mean():.0%} of clients, right {y[high].mean():.0%} of the time")
    print("\nWhat this shows: accuracy cannot see overconfidence, because it only looks at which side of\n"
          "50% a probability falls. Proper scoring rules (log loss, Brier) reward honest probabilities.\n"
          "Any layer whose probabilities drive decisions, such as the refer-to-human rule in U2, should\n"
          "be trained and judged on one.")


if __name__ == "__main__":
    main()
