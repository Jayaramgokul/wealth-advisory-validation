"""D3. Input drift, not just output drift.

Research: Gebru et al. (2021); Yurdakul (2018) on the Population Stability Index.
Document: 03-research/data-fitness.md

Question: after a marketing campaign, new clients are younger and less
experienced. The mix of recommended portfolios barely moves. Is the model
still working on the population it was built for?

    python 05-illustrations/d3_input_drift_psi.py
"""

import numpy as np
import pandas as pd

from common import answer_score, bucket, psi, questionnaire

WATCH, ACT = 0.10, 0.25        # common rule-of-thumb PSI bands; see the research note on their limits


def main():
    reference = questionnaire(seed=0)
    live = questionnaire(seed=1, age_mean=36, novice_share=0.80)
    rows = []
    for name, a, b in [("age", reference["age"], live["age"]),
                       ("experienced (share)", (reference["experience"] == "experienced").astype(float),
                        (live["experience"] == "experienced").astype(float)),
                       ("questionnaire score", answer_score(reference), answer_score(live))]:
        a, b = pd.Series(a), pd.Series(b)
        if a.nunique() <= 2:                                   # binary input: compare the two shares directly
            e = np.clip([1 - a.mean(), a.mean()], 1e-6, None)
            o = np.clip([1 - b.mean(), b.mean()], 1e-6, None)
            value = float(np.sum((o - e) * np.log(o / e)))
        else:
            value = psi(a, b)
        rows.append((name, value))
    ref_b, live_b = bucket(answer_score(reference)), bucket(answer_score(live))
    e = np.bincount(ref_b, minlength=5) / len(ref_b)
    o = np.bincount(live_b, minlength=5) / len(live_b)
    rows.append(("recommended bucket (output)", float(np.sum((o - e) * np.log(np.clip(o, 1e-6, None) / e)))))

    print("Population Stability Index, reference clients against new clients (simulated)\n")
    for name, value in rows:
        flag = "act" if value >= ACT else "watch" if value >= WATCH else "stable"
        print(f"{name:30s} PSI {value:5.3f}   {flag}")
    print("\nBucket mix, reference vs live:", pd.Series(e).round(2).tolist(), "vs", pd.Series(o).round(2).tolist())
    print("\nWhat this shows: younger clients would score higher and novices lower, so the two shifts\n"
          "partly cancel in the output. An output-only monitor would stay quiet while the population the\n"
          "model was validated on has changed. Monitor the inputs, and treat the PSI bands as triggers for\n"
          "review, not as tests with known error rates.")


if __name__ == "__main__":
    main()
