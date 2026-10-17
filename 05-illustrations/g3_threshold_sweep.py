"""G3. Thresholds and who they affect.

Research: Buolamwini & Gebru (2018); Barocas et al. (2021).
Document: 03-research/groups-an-average-hides.md

Question: clients scoring above a cut-off are offered the highest-risk band
(Band 5). Among clients for whom it is not suitable, how many are offered it
anyway, for novice and experienced investors, as the cut-off moves?

    python 05-illustrations/g3_threshold_sweep.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from common import answer_score, questionnaire, save  # noqa: E402

SUITABLE_FROM = 75          # true tolerance at which Band 5 is suitable


def main():
    clients = questionnaire(n=20000)
    score = answer_score(clients)
    suitable = (clients["true_tolerance"] >= SUITABLE_FROM).to_numpy()
    cuts = np.arange(60, 91, 1)
    rates = {}
    for g in ["novice", "experienced"]:
        m = (clients["experience"] == g).to_numpy()
        unsuitable = m & ~suitable
        rates[g] = [np.mean(score[unsuitable] >= c) for c in cuts]
    print("Of clients for whom Band 5 is NOT suitable, the share offered it anyway (simulated)\n")
    print(f"{'cut-off':>8s} {'novice':>8s} {'experienced':>12s}")
    for c in (65, 70, 75, 80, 85):
        i = int(np.where(cuts == c)[0][0])
        print(f"{c:8d} {rates['novice'][i]:8.1%} {rates['experienced'][i]:12.1%}")
    gap = np.array(rates["novice"]) - np.array(rates["experienced"])
    cross = cuts[np.argmax(gap > 0)] if (gap > 0).any() else None
    print(f"\nNovices bear more of the cost from a cut-off of about {cross} upwards." if cross else "")
    print("\nWhat this shows: who bears the cost of a threshold depends on where it sits. Low cut-offs catch\n"
          "experienced clients who sit just below the suitability line; high cut-offs mostly catch novices,\n"
          "whose noisier answers push a few far above their true tolerance. A threshold chosen on the overall\n"
          "error rate says nothing about this, so the chosen one should be justified against this curve.")

    fig, ax = plt.subplots(figsize=(6, 3))
    for g, r in rates.items():
        ax.plot(cuts, r, label=g)
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    ax.set_xlabel("Score cut-off for Band 5")
    ax.set_ylabel("Offered, though unsuitable")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    print(f"\nChart: {save(fig, 'g3_threshold_sweep')}")


if __name__ == "__main__":
    main()
