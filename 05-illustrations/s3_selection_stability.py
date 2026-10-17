"""S3. Feature-selection stability.

Research: Hastie, Tibshirani & Friedman (2009), section 3.4 (the lasso); Meinshausen & Buhlmann
(2010), stability selection.
Document: 03-research/statistical-rigour.md

Question: client material says the model's recommendations are "driven by"
a short list of factors chosen by a lasso fit. Would the same list come out
if the data were slightly different?

    python 05-illustrations/s3_selection_stability.py
"""

import numpy as np
from sklearn.linear_model import Lasso, LassoCV
from sklearn.preprocessing import StandardScaler

NAMES = ["income", "savings rate", "horizon", "age", "dependants", "debt ratio", "experience", "home owner",
         "employment years", "liquid assets", "pension", "region index"]
BOOTSTRAPS = 200


def main():
    rng = np.random.default_rng(0)
    n = 300
    base = rng.normal(size=(n, len(NAMES)))
    base[:, 9] = 0.85 * base[:, 0] + 0.5 * rng.normal(size=n)       # liquid assets track income
    base[:, 3] = -0.8 * base[:, 2] + 0.6 * rng.normal(size=n)       # age moves against horizon
    X = StandardScaler().fit_transform(base)
    y = 0.5 * X[:, 0] + 0.5 * X[:, 2] + 0.25 * X[:, 6] + rng.normal(0, 1.2, n)

    alpha = LassoCV(cv=5, random_state=0).fit(X, y).alpha_
    single = np.abs(Lasso(alpha=alpha).fit(X, y).coef_) > 1e-8
    freq = np.zeros(len(NAMES))
    for _ in range(BOOTSTRAPS):
        s = rng.integers(0, n, n)
        freq += np.abs(Lasso(alpha=alpha).fit(X[s], y[s]).coef_) > 1e-8
    freq /= BOOTSTRAPS
    print("Factors selected by one lasso fit, and how often each is selected across 200 resamples\n")
    for i in np.argsort(-freq):
        print(f"{NAMES[i]:17s} {'in disclosed list' if single[i] else '':18s} selected in {freq[i]:4.0%} of resamples")
    print("\nWhat this shows: correlated factors take turns being chosen, so a single fit's list is partly\n"
          "luck. Only factors selected in a high share of resamples (agreed in advance) should be\n"
          "described to clients as what drives the advice.")


if __name__ == "__main__":
    main()
