"""Checks that the shared statistics are right and that every illustration runs.

    python -m pytest tests/ -q
"""

import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ILLUSTRATIONS = Path(__file__).resolve().parents[1] / "05-illustrations"
sys.path.insert(0, str(ILLUSTRATIONS))

import common  # noqa: E402


def test_wilson_contains_rate_and_handles_zero():
    lo, hi = common.wilson(30, 100)
    assert lo < 0.30 < hi
    lo, hi = common.wilson(0, 50)
    assert lo == 0.0 and 0 < hi < 0.1


def test_bh_matches_hand_calculation():
    # Sorted p 0.01, 0.03, 0.04, 0.20 -> p*n/rank 0.04, 0.06, 0.0533, 0.20 -> running minimum from the top.
    q = common.bh([0.01, 0.04, 0.03, 0.20])
    assert np.allclose(q, [0.04, 0.16 / 3, 0.16 / 3, 0.20])


def test_psi_near_zero_for_same_distribution_and_large_for_shift():
    rng = np.random.default_rng(0)
    a = rng.normal(0, 1, 5000)
    assert common.psi(a, rng.normal(0, 1, 5000)) < 0.02
    assert common.psi(a, rng.normal(1, 1, 5000)) > 0.25


def test_cronbach_alpha_high_for_consistent_items_low_for_noise():
    rng = np.random.default_rng(0)
    latent = rng.normal(0, 1, 2000)
    consistent = pd.DataFrame({f"q{i}": latent + rng.normal(0, 0.3, 2000) for i in range(6)})
    noise = pd.DataFrame({f"q{i}": rng.normal(0, 1, 2000) for i in range(6)})
    assert common.cronbach_alpha(consistent) > 0.9
    assert abs(common.cronbach_alpha(noise)) < 0.1


def test_smallest_detectable_gap_shrinks_with_sample_size():
    assert common.smallest_detectable_gap(0.5, 50, 5000) > common.smallest_detectable_gap(0.5, 2000, 5000)


def test_block_bootstrap_keeps_consecutive_days_together():
    idx = common.block_bootstrap_index(1000, 20, 5, np.random.default_rng(0))
    assert idx.shape == (5, 1000)
    assert np.all(np.diff(idx[:, :20], axis=1) == 1)


def test_market_returns_bonds_rally_in_crisis():
    m = common.market_returns(years=10)
    crisis = m[m["regime"] == "crisis"]
    assert crisis["equity"].mean() < 0 < crisis["bonds"].mean()


@pytest.mark.parametrize("script", sorted(p.name for p in ILLUSTRATIONS.glob("[a-z][0-9]_*.py")))
def test_illustration_runs(script):
    result = subprocess.run([sys.executable, script], cwd=ILLUSTRATIONS, capture_output=True, text=True,
                            timeout=600, env={**os.environ, "MPLBACKEND": "Agg"})
    assert result.returncode == 0, result.stderr
    assert "What this shows" in result.stdout
