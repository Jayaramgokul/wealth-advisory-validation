"""S2. Multiple testing across the suite.

Research: Benjamini & Hochberg (1995); Hastie, Tibshirani & Friedman (2009), section 18.7.
Document: 03-research/statistical-rigour.md

Question: a validation compares the suitability rate of 300 client segments
with the overall rate. Ten segments are genuinely worse. How many findings
are real if each test is read at p < 0.05?

    python 05-illustrations/s2_multiple_testing.py
"""

import numpy as np
from scipy import stats

from common import bh

SEGMENTS, REAL, BASE, WORSE = 300, 10, 0.80, 0.68


def main():
    rng = np.random.default_rng(0)
    size = rng.integers(150, 400, SEGMENTS)
    rate = np.full(SEGMENTS, BASE)
    rate[:REAL] = WORSE                                    # the first ten segments are genuinely worse
    ok = rng.binomial(size, rate)
    p = np.array([stats.binomtest(int(k), int(n), BASE, alternative="less").pvalue for k, n in zip(ok, size)])
    real = np.arange(SEGMENTS) < REAL
    for label, flagged in (("each test at p < 0.05", p < 0.05), ("false discovery rate 5% (BH)", bh(p) < 0.05)):
        print(f"{label:30s} flagged {flagged.sum():3d}: {np.sum(flagged & real):2d} real, "
              f"{np.sum(flagged & ~real):2d} false alarms")
    print("\nWhat this shows: with hundreds of slices, chance alone produces a stream of 'failures' that\n"
          "bury the real ones and erode trust in the suite. Controlling the false discovery rate across\n"
          "the whole suite keeps most real findings and removes most false alarms.")


if __name__ == "__main__":
    main()
