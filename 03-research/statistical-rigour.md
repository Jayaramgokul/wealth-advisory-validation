# Statistical rigour

> Public sources only; full references in [SOURCES.md](../SOURCES.md). Every
> number quoted below comes from the simulated data in
> [05-illustrations](../05-illustrations/), not from any real firm.

## Why this lens

Every other lens produces numbers: rates, gaps, intervals, p-values. This one
asks whether those numbers are honest. *The Elements of Statistical Learning*
(Hastie, Tibshirani & Friedman) catalogues the classic ways validation
numbers mislead: choices made on the full dataset leaking into
cross-validation, "important" features that are artefacts of one sample,
error rates that mix up bias and variance, and real findings buried under
chance ones when many tests are run.

A validation suite like this one, with dozens of tests each split by group
and bucket, is exactly where those problems arise. So this lens applies to
the validation itself as much as to the model.

## What I read, and what each source changed

| Source | The idea I took from it | What it changed in the tests |
|---|---|---|
| Hastie et al. (2009), section 7.10.2, *the wrong and right way to do cross-validation* | Any step that uses the outcome (such as feature screening) must be repeated inside each fold. | Re-run every data-driven step inside the folds (S1) |
| Benjamini & Hochberg (1995); Hastie et al. (2009), section 18.7 | Control the false discovery rate when many hypotheses are tested. | FDR control across the whole suite (S2) |
| Hastie et al. (2009), section 3.4; Meinshausen & Bühlmann (2010) | Lasso selection among correlated features is unstable; selection frequency under resampling is more reliable. | Disclosed drivers must be stable under resampling (S3) |
| Hastie et al. (2009), sections 7.3 and 7.6 | Error decomposes into bias, variance and noise; effective degrees of freedom measure how much a model has fitted. | Bias-variance decomposition (S4); complexity against data (S5) |

## The tests

---

### S1. Nested cross-validation

**Principle.** If features, thresholds or tuning are chosen using all the
data, cross-validation afterwards measures how well the model fits data it
has partly seen (Hastie et al., 7.10.2).

**Objective.** Check that the performance reported in model documentation
comes from a procedure in which every data-driven choice was repeated inside
each fold.

**Client harm.** A model is approved on accuracy it does not have.

**Why existing tests miss it.** The cross-validation code is usually correct.
The leak is in the steps before it, which may sit in a different notebook or
team.

**Data.** The full development pipeline, from raw features to final model.

**Method.**
1. List every step that uses the outcome: screening, selection, tuning,
   threshold setting.
2. Rebuild the pipeline so all of them run inside each training fold.
3. Compare the nested estimate with the documented one.

**Setting the pass criteria.** The documented performance is the nested
figure, or the gap is explained and immaterial.

**What the illustration shows.** With a random outcome (true accuracy 50%),
choosing 20 of 2,000 features on all the data and then cross-validating
reports 76%. Repeating the choice inside each fold gives 52%.
[`s1_nested_cross_validation.py`](../05-illustrations/s1_nested_cross_validation.py)

**Regulatory hook.** SR 26-2 (outcomes analysis). **NIST AI RMF.** MEASURE 2.5.

---

### S2. Multiple testing across the suite

**Principle.** At p < 0.05, one test in twenty of a true null "fails" by
chance. The false discovery rate controls the share of flagged results that
are false (Benjamini & Hochberg, 1995).

**Objective.** Report pass and fail across the whole suite with the false
discovery rate controlled, so findings can be trusted.

**Client harm.** Real problems are lost among false alarms, or the suite is
dismissed as noisy and real failures are ignored.

**Why existing tests miss it.** Each test is designed and read on its own.
Nobody counts how many were run.

**Data.** Every p-value the suite produces, collected in one table.

**Method.**
1. Gather all p-values: every test, group and bucket.
2. Apply Benjamini-Hochberg at the agreed rate.
3. Report findings from the corrected table only. Keep uncorrected results
   as exploratory (F7).

**Setting the pass criteria.** Every pass or fail statement in the report is
backed by the corrected table.

**What the illustration shows.** Of 300 segments, 10 are genuinely worse.
Reading each test at p < 0.05 flags 15: 9 real and 6 false alarms. With the
false discovery rate controlled at 5%, the suite flags 9, all real.
[`s2_multiple_testing.py`](../05-illustrations/s2_multiple_testing.py)

**Regulatory hook.** SR 26-2 (effective challenge). **NIST AI RMF.** MEASURE 2.13.

---

### S3. Feature-selection stability

**Principle.** When features are correlated, the lasso picks one of a
correlated set somewhat arbitrarily; the choice changes with the sample.
Selection frequency across resamples separates stable drivers from lucky
ones (Meinshausen & Bühlmann, 2010).

**Objective.** Check that any factor described to clients or governance as
"driving" the model is selected consistently under resampling.

**Client harm.** Clients are told their advice depends on factors that a
slightly different dataset would not have chosen. The explanation is not
reliable.

**Why existing tests miss it.** The feature list comes from one fit and is
reviewed for plausibility, not stability.

**Data.** The development data and the selection procedure.

**Method.**
1. Repeat the selection on many bootstrap resamples with the same settings.
2. Record how often each feature is selected.
3. Compare with the disclosed list.

**Setting the pass criteria.** Every disclosed driver is selected in at
least an agreed share of resamples (for example, 80%).

**What the illustration shows.** One lasso fit selects six factors. Across
200 resamples, only income and horizon are selected every time; experience
76%; savings rate, home ownership and liquid assets between 48% and 60%.
Liquid assets track income, and the two take turns.
[`s3_selection_stability.py`](../05-illustrations/s3_selection_stability.py)

**Regulatory hook.** Disclosure of how the algorithm works (SEC IM Guidance
2017-02). **NIST AI RMF.** MEASURE 2.9.

---

### S4. Bias-variance decomposition

**Objective, method and pass criteria.** Refit the model on bootstrap
resamples and split its error, per risk bucket, into bias (systematically
wrong), variance (unstable) and noise (Hastie et al., 7.3). Pass if the
dominant source is identified for every bucket that misses its target.

**Client harm.** The wrong fix is applied: more data for a model that is
biased, or a more complex model when the problem is instability.

**Regulatory hook.** SR 26-2 (outcomes analysis). **NIST AI RMF.** MEASURE 2.5.

### S5. Effective complexity against data

**Objective, method and pass criteria.** Estimate effective degrees of
freedom for each component (Hastie et al., 7.6) and compare with the size of
the validation data. Pass if the ratio is within an agreed limit, or a
written justification exists.

**Client harm.** A model too flexible for its data looks good in validation
and disappoints in use.

**Regulatory hook.** SR 26-2 (conceptual soundness). **NIST AI RMF.** MEASURE 2.5.

## How the tests fit together

S1 and S5 ask whether reported performance is real. S3 and S4 ask whether
what the model is said to do is stable. S2 applies to the whole validation
and should be the last step before any report.
