"""S1. Nested cross-validation.

Research: Hastie, Tibshirani & Friedman (2009), section 7.10.2, "The wrong and right way to do
cross-validation".
Document: 03-research/statistical-rigour.md

Question: a model predicting which clients will need a portfolio change was
built by first picking the 20 most predictive of 2,000 candidate features,
then cross-validating. Is the reported accuracy real?

Here the outcome is pure noise, so the true accuracy of any model is 50%.

    python 05-illustrations/s1_nested_cross_validation.py
"""

import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline


def main():
    rng = np.random.default_rng(0)
    X = rng.normal(size=(200, 2000))
    y = rng.integers(0, 2, 200)
    folds = StratifiedKFold(5, shuffle=True, random_state=0)

    chosen = SelectKBest(f_classif, k=20).fit(X, y).get_support()         # selection sees every client
    wrong = cross_val_score(LogisticRegression(max_iter=1000), X[:, chosen], y, cv=folds).mean()
    right = cross_val_score(make_pipeline(SelectKBest(f_classif, k=20), LogisticRegression(max_iter=1000)),
                            X, y, cv=folds).mean()                        # selection redone inside each fold
    print("Outcome is random, so the honest answer is 50%.\n")
    print(f"Features chosen on all data, then cross-validated: {wrong:.0%}")
    print(f"Feature choice repeated inside each fold:          {right:.0%}")
    print("\nWhat this shows: any choice made with the full dataset (features, thresholds, tuning) leaks the\n"
          "test folds into the model. The validator re-runs every data-driven step inside the folds and\n"
          "compares the result with the number in the model documentation.")


if __name__ == "__main__":
    main()
