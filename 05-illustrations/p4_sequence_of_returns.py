"""P4. Sequence-of-returns risk for retirees.

Research: Bengen (1994).
Document: 03-research/portfolio-risk-and-performance.md

Question: two retirees earn exactly the same returns, in a different order.
Does one run out of money?

    python 05-illustrations/p4_sequence_of_returns.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from common import MODEL_PORTFOLIOS, TRADING_DAYS, market_returns, portfolio_returns, save  # noqa: E402

WITHDRAWAL, YEARS, PATHS = 0.04, 30, 5000


def wealth_path(annual, withdrawal=WITHDRAWAL):
    w, path = 1.0, []
    for g in annual:
        w = max(0.0, w * (1 + g) - withdrawal)
        path.append(w)
    return np.array(path)


def main():
    rng = np.random.default_rng(0)
    m = market_returns(years=YEARS)
    print(f"Withdrawing {WITHDRAWAL:.0%} of the starting value each year for {YEARS} years (simulated data)\n")
    shown = {}
    for name in MODEL_PORTFOLIOS:
        r = portfolio_returns(m, name)
        annual = (1 + r.to_numpy()).reshape(YEARS, TRADING_DAYS).prod(axis=1) - 1     # 252-day years
        # Exactly the same annual returns, shuffled into many different orders.
        orders = np.array([rng.permutation(annual) for _ in range(PATHS)])
        ends = np.array([wealth_path(o)[-1] for o in orders])
        print(f"{name:12s} average annual return {annual.mean():5.1%}   runs out in {np.mean(ends == 0):5.1%} of orderings")
        if name == "85/15":
            worst = orders[np.argmin([wealth_path(o).sum() for o in orders])]
            best = orders[np.argmax([wealth_path(o).sum() for o in orders])]
            shown = {"bad years first": wealth_path(worst), "good years first": wealth_path(best)}
    print("\nWhat this shows: the average return is identical in every ordering, yet outcomes differ\n"
          "sharply. Losses early in retirement, while withdrawals continue, do lasting damage. Advice and\n"
          "disclosures for clients drawing an income should be tested on orderings, not averages.")

    fig, ax = plt.subplots(figsize=(6, 3))
    for label, path in shown.items():
        ax.plot(np.arange(1, YEARS + 1), path, label=label)
    ax.set_xlabel("Year of retirement")
    ax.set_ylabel("Wealth (start = 1)")
    ax.legend(frameon=False)
    ax.set_title("85/15 portfolio: same returns, different order", loc="left", fontsize=9)
    ax.spines[["top", "right"]].set_visible(False)
    print(f"\nChart: {save(fig, 'p4_sequence_of_returns')}")


if __name__ == "__main__":
    main()
