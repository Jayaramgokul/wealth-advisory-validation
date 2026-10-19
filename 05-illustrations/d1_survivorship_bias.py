"""D1. Survivorship bias in backtest data.

Research: Gebru et al. (2021), Datasheets for Datasets (what is left out of the data?).
Document: 03-research/data-fitness.md

Question: a backtest is built from the funds that exist today. How much better
does it look than the results an investor could actually have had, when
funds that closed along the way are put back in?

    python 05-illustrations/d1_survivorship_bias.py
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from common import save  # noqa: E402

FUNDS, YEARS = 400, 10
CLOSE_BELOW = 0.85           # a fund is closed once it trails the market by 15% since launch


def main():
    rng = np.random.default_rng(0)
    months = YEARS * 12
    skill = rng.normal(-0.005, 0.02, FUNDS)                     # annual alpha after fees: some good, most not
    market = rng.normal(0.07 / 12, 0.045, months)
    r = market + skill[:, None] / 12 + rng.normal(0, 0.015, (FUNDS, months))
    alive = np.ones(FUNDS, bool)
    full = np.full((FUNDS, months), np.nan)                     # what an investor could have held
    for t in range(months):
        full[alive, t] = r[alive, t]
        relative = np.nanprod(1 + full[:, : t + 1], axis=1) / np.prod(1 + market[: t + 1])
        alive &= relative >= CLOSE_BELOW
    survivors = alive

    def annual(rows):
        monthly = np.nanmean(full[rows], axis=0)                 # equal-weighted across funds alive each month
        return (np.prod(1 + monthly)) ** (1 / YEARS) - 1

    everyone = np.ones(FUNDS, bool)
    s, f = annual(survivors), annual(everyone)
    print(f"{FUNDS} simulated funds over {YEARS} years; {FUNDS - survivors.sum()} closed along the way.\n")
    print(f"Backtest on today's survivors only : {s:6.2%} a year")
    print(f"Backtest on the full universe      : {f:6.2%} a year")
    print(f"Survivorship bias                  : {s - f:+6.2%} a year, {(1 + s) ** YEARS / (1 + f) ** YEARS - 1:+.1%} "
          f"over {YEARS} years")
    print("\nWhat this shows: funds disappear because they did badly, so a universe built from today's list\n"
          "quietly drops the worst results. A backtest shown to clients should be rebuilt on the universe\n"
          "that existed at each date, and the datasheet should say how closed products were handled.")
    fig, ax = plt.subplots(figsize=(6, 2.8))
    years = np.arange(1, months + 1) / 12
    for rows, label in ((survivors, "today's survivors only"), (everyone, "every fund that existed at the time")):
        ax.plot(years, np.cumprod(1 + np.nanmean(full[rows], axis=0)), label=label)
    ax.set_xlabel("Years")
    ax.set_ylabel("Growth of 1 (equal-weighted)")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    print(f"\nChart: {save(fig, 'd1_survivorship')}")


if __name__ == "__main__":
    main()
