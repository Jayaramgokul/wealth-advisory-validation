"""Shared helpers for the illustration scripts: dummy data and small statistics.

Every number these scripts produce comes from simulated data. The point is to
show how each test works and why it matters, not to describe any real firm.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(exist_ok=True)
TRADING_DAYS = 252

# ---------------------------------------------------------------- dummy data

ASSETS = ["equity", "bonds", "cash"]
MODEL_PORTFOLIOS = {                # named equity / everything else; weights in equity, bonds, cash
    "20/80": [0.20, 0.60, 0.20],
    "50/50": [0.50, 0.45, 0.05],
    "85/15": [0.85, 0.14, 0.01],
}
DISCLOSED_VOL = {"20/80": 0.06, "50/50": 0.11, "85/15": 0.17}   # stated annual volatility band


def market_returns(years: int = 20, seed: int = 1) -> pd.DataFrame:
    """Daily returns with calm and crisis regimes and fat tails.

    In a crisis, equities fall and become more volatile, high-quality bonds
    rally, and a common fat-tailed shock hits everything at once.
    """
    rng = np.random.default_rng(seed)
    days = years * TRADING_DAYS
    crisis = np.zeros(days, bool)
    state = False
    for d in range(days):                                       # two-state Markov chain
        state = rng.random() < (0.97 if state else 0.004)
        crisis[d] = state
    mu = {"calm": np.array([0.08, 0.03, 0.02]), "crisis": np.array([-0.30, 0.06, 0.02])}
    vol = {"calm": np.array([0.14, 0.05, 0.005]), "crisis": np.array([0.40, 0.07, 0.005])}
    corr = {"calm": np.array([[1, 0.1, 0], [0.1, 1, 0.1], [0, 0.1, 1]]),
            "crisis": np.array([[1, -0.3, 0], [-0.3, 1, 0.1], [0, 0.1, 1]])}
    out = np.empty((days, 3))
    for regime, mask in (("calm", ~crisis), ("crisis", crisis)):
        k = int(mask.sum())
        if not k:
            continue
        s = vol[regime] / np.sqrt(TRADING_DAYS)
        z = rng.multivariate_normal(np.zeros(3), np.outer(s, s) * corr[regime], k)
        shock = np.abs(rng.standard_t(4, (k, 1))) / np.sqrt(2)  # fat tails
        out[mask] = mu[regime] / TRADING_DAYS + z * shock
    df = pd.DataFrame(out, index=pd.bdate_range("2005-01-03", periods=days), columns=ASSETS)
    df["regime"] = np.where(crisis, "crisis", "calm")
    return df


def portfolio_returns(m: pd.DataFrame, name: str) -> pd.Series:
    return (m[ASSETS] * MODEL_PORTFOLIOS[name]).sum(axis=1)


def questionnaire(n: int = 4000, seed: int = 0, novice_noise: float = 1.3, experienced_noise: float = 0.6,
                  items: int = 8, age_mean: float = 45, novice_share: float = 0.4) -> pd.DataFrame:
    """Risk-questionnaire answers (1-5) driven by a latent risk tolerance.

    Novice investors answer less consistently, so the same questions measure
    them with more error.
    """
    rng = np.random.default_rng(seed)
    experience = np.where(rng.random(n) < novice_share, "novice", "experienced")
    region = rng.choice(["north", "south", "east", "west"], n)
    sex = rng.choice(["female", "male"], n)
    age = np.clip(rng.normal(age_mean, 13, n), 21, 85).round()
    latent = np.clip(70 - 0.6 * (age - 21) + 8 * (experience == "experienced") + rng.normal(0, 10, n), 0, 100)
    noise = np.where(experience == "novice", novice_noise, experienced_noise)
    answers = {f"q{i + 1}": np.clip(np.round(3 + 0.65 * (latent - 50) / 15 + rng.normal(0, 1, n) * noise), 1, 5)
               for i in range(items)}
    return pd.DataFrame({"age": age, "sex": sex, "region": region, "experience": experience,
                         "true_tolerance": latent, **answers})


QUESTIONS = [f"q{i}" for i in range(1, 9)]
BUCKETS = ["Band 1", "Band 2", "Band 3", "Band 4", "Band 5"]   # lowest to highest risk
CUTOFFS = [30, 45, 60, 75]                   # 0-100 score -> one of five buckets


def answer_score(c: pd.DataFrame) -> np.ndarray:
    """Questionnaire score on 0-100: the simple average of the answers."""
    return (c[QUESTIONS].to_numpy() - 1).mean(axis=1) / 4 * 100


def bucket(scores) -> np.ndarray:
    return np.searchsorted(CUTOFFS, np.asarray(scores), side="right")


# ---------------------------------------------------------------- statistics


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for a proportion."""
    if n == 0:
        return 0.0, 1.0
    p = k / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return max(0.0, centre - half), min(1.0, centre + half)


def bh(p) -> np.ndarray:
    """Benjamini-Hochberg adjusted p-values."""
    p = np.asarray(p, float)
    order = np.argsort(p)
    ranked = p[order] * len(p) / np.arange(1, len(p) + 1)
    q = np.minimum.accumulate(ranked[::-1])[::-1]
    out = np.empty_like(q)
    out[order] = np.minimum(q, 1.0)
    return out


def psi(expected, actual, bins: int = 10) -> float:
    """Population Stability Index, decile bins of the expected sample."""
    e_, a_ = np.asarray(expected, float), np.asarray(actual, float)
    edges = np.unique(np.quantile(e_, np.linspace(0, 1, bins + 1)))
    edges[0], edges[-1] = -np.inf, np.inf
    e = np.clip(np.histogram(e_, edges)[0] / len(e_), 1e-6, None)
    a = np.clip(np.histogram(a_, edges)[0] / len(a_), 1e-6, None)
    return float(np.sum((a - e) * np.log(a / e)))


def cronbach_alpha(items: pd.DataFrame) -> float:
    """Internal-consistency reliability of a set of questionnaire items."""
    x = items.to_numpy(float)
    k = x.shape[1]
    return float(k / (k - 1) * (1 - x.var(axis=0, ddof=1).sum() / x.sum(axis=1).var(ddof=1)))


def block_bootstrap_index(T: int, block: int, n: int, rng) -> np.ndarray:
    """Indices for moving-block bootstrap samples (keeps short-range dependence)."""
    starts = rng.integers(0, T - block, (n, int(np.ceil(T / block))))
    return (starts[:, :, None] + np.arange(block)).reshape(n, -1)[:, :T]


def smallest_detectable_gap(p: float, n1: int, n2: int, alpha: float = 0.05, power: float = 0.8) -> float:
    """Smallest difference in a rate that two groups of these sizes could detect."""
    z = stats.norm.ppf(1 - alpha / 2) + stats.norm.ppf(power)
    return float(z * math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2)))


def save(fig, name: str) -> Path:
    path = OUT / f"{name}.png"
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    return path
