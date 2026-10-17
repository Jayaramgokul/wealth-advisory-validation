"""D7. Label noise and rater agreement.

Research: Gebru et al. (2021); Cohen (1960, 1968) on kappa.
Document: 03-research/data-fitness.md

Question: the "correct" risk bucket for a sample of client files was set by
reviewers, and those labels are used to judge the model. Would two reviewers
give the same label?

    python 05-illustrations/d7_rater_agreement.py
"""

import numpy as np

K = 5   # five risk buckets


def kappa(a, b, weights=None):
    """Cohen's kappa; weights='quadratic' gives the weighted version for ordered labels."""
    obs = np.zeros((K, K))
    np.add.at(obs, (a, b), 1)
    obs /= obs.sum()
    exp = np.outer(obs.sum(1), obs.sum(0))
    i, j = np.indices((K, K))
    w = ((i - j) / (K - 1)) ** 2 if weights == "quadratic" else (i != j).astype(float)
    return 1 - (w * obs).sum() / (w * exp).sum()


def main():
    rng = np.random.default_rng(0)
    n = 300
    truth = rng.normal(0, 1, n)
    cut = [-1.2, -0.4, 0.4, 1.2]
    rater_a = np.digitize(truth + rng.normal(0, 0.45, n), cut)
    rater_b = np.digitize(truth + rng.normal(0, 0.45, n), cut)
    boot = []
    for _ in range(1000):
        s = rng.integers(0, n, n)
        boot.append(kappa(rater_a[s], rater_b[s]))
    lo, hi = np.quantile(boot, [0.025, 0.975])
    print(f"Two reviewers label the same {n} simulated client files into five risk buckets\n")
    print(f"Raw agreement            {np.mean(rater_a == rater_b):.0%}")
    print(f"Cohen's kappa            {kappa(rater_a, rater_b):.2f}   (95% CI {lo:.2f} to {hi:.2f})")
    print(f"Weighted kappa           {kappa(rater_a, rater_b, 'quadratic'):.2f}   (near misses count less)")
    print(f"Disagreements one bucket apart: {np.mean(np.abs(rater_a - rater_b)[rater_a != rater_b] == 1):.0%}")
    print("\nWhat this shows: raw agreement flatters, because some agreement happens by chance; kappa\n"
          f"removes that. Here reviewers disagree on {np.mean(rater_a != rater_b):.0%} of files, mostly by one bucket. "
          "Against labels\nlike these, a model's 'accuracy' partly measures the reviewers, so agreement must be "
          "known before\naccuracy is judged, and boundary cases need a second review.")


if __name__ == "__main__":
    main()
