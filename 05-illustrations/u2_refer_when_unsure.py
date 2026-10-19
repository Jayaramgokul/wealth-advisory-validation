"""U2. Refer to a human when unsure.

Research: Bishop (2006), section 1.5.3 (the reject option).
Document: 03-research/decisions-under-uncertainty.md

Question: for some clients the questionnaire cannot tell which bucket they
belong in. If a human review costs something, which clients should be
referred, and how much harm does that avoid?

    python 05-illustrations/u2_refer_when_unsure.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from common import answer_score, bucket, questionnaire, save  # noqa: E402
from u1_cost_of_mistakes import COST, K  # noqa: E402

REVIEW_COSTS = [0.4, 0.6, 0.8]       # cost of a human review, in the same units as the cost matrix


def cell(c, bins):
    """Score bin, kept separate for novice and experienced clients (the model knows which is which)."""
    return np.digitize(answer_score(c), bins) + (len(bins) + 1) * (c["experience"] == "novice").to_numpy()


def posterior(calib, bins):
    """P(true bucket | score bin, experience), estimated on a separate calibration sample."""
    table = np.ones((2 * (len(bins) + 1), K))                        # add-one smoothing
    np.add.at(table, (cell(calib, bins), bucket(calib["true_tolerance"])), 1)
    return table / table.sum(1, keepdims=True)


def main():
    bins = np.linspace(0, 100, 41)[1:-1]
    post = posterior(questionnaire(n=40000, seed=5), bins)
    clients = questionnaire(n=6000, seed=6)
    p = post[cell(clients, bins)]                                    # one row of probabilities per client
    true = bucket(clients["true_tolerance"])
    expected = p @ COST.T                                            # expected cost of each placement
    best = expected.argmin(1)
    novice = (clients["experience"] == "novice").to_numpy()
    print("Refer a client when the lowest expected cost of any placement exceeds the cost of a review\n")
    print(f"Always place: expected cost {COST[best, true].mean():.2f} per client\n")
    print(f"{'review cost':>11s} {'expected cost':>14s} {'referred':>9s} {'novices':>8s} {'experienced':>12s}")
    for rc in REVIEW_COSTS:
        refer = expected.min(1) > rc
        cost = np.where(refer, rc, COST[best, true]).mean()
        print(f"{rc:11.1f} {cost:14.2f} {refer.mean():9.0%} {refer[novice].mean():8.0%} {refer[~novice].mean():12.0%}")
    print("\nWhat this shows: a model that always answers spends its mistakes on the clients it understands\n"
          "least. A refer-to-human rule, set from the cost matrix and the model's own uncertainty, puts\n"
          "review effort where it saves most harm. How many referrals are affordable is a business choice;\n"
          "the rule makes the trade-off visible.")
    # Refer the clients the model is least sure about first, and trace the cost as the share referred grows.
    order = np.argsort(-expected.min(1))
    realised = COST[best, true][order]
    n = len(order)
    remaining = np.r_[np.cumsum(realised[::-1])[::-1], 0]               # cost of placing everyone not referred
    fig, ax = plt.subplots(figsize=(6, 3))
    for rc, colour in zip(REVIEW_COSTS, ("#3182bd", "#ff7f0e", "#2ca02c")):
        ax.plot(np.arange(n + 1) / n, (rc * np.arange(n + 1) + remaining) / n, color=colour,
                label=f"review cost {rc:.1f}")
        m = int((expected.min(1) > rc).sum())
        ax.plot(m / n, (rc * m + remaining[m]) / n, "o", color=colour)
    ax.set_xlim(0, 0.8)
    ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    ax.set_xlabel("Share of clients referred (least certain first); dot = the rule's choice")
    ax.set_ylabel("Cost per client")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    print(f"\nChart: {save(fig, 'u2_refer_when_unsure')}")


if __name__ == "__main__":
    main()
