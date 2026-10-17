# Reliability when the world shifts

> Public sources only; full references in [SOURCES.md](../SOURCES.md). Every
> number quoted below comes from the simulated data in
> [05-illustrations](../05-illustrations/), not from any real firm.

## Why this lens

A validation is a snapshot. The model then runs in a world where client mix,
markets and the model's own influence keep changing. Saria and Subbaswamy's
tutorial on safe and reliable machine learning organises the risks into
failures to *prevent*, to *detect* and to *maintain against*, with dataset
shift at the centre. Their practical advice is to write down which
relationships in the data could change between the environment the model was
built in and the one it is used in, and to test for those specifically.

There is a statistical side too. Market data and client data are not
independent observations: bad days cluster, and clients onboarded in the same
campaign resemble each other. Methods that assume independence give
intervals that are too narrow, so conclusions look more certain than they are.

## What I read, and what each source changed

| Source | The idea I took from it | What it changed in the tests |
|---|---|---|
| Saria & Subbaswamy (2019), *Safe and Reliable Machine Learning* | Reason explicitly about which relationships can shift between environments; monitor and maintain against them. | A written diagram of shifts that matter (R2); testing transfer (R3); feedback loops (R4); misspecification (R5) |
| Künsch (1989); Efron (1979) | The block bootstrap keeps short-range dependence that the ordinary bootstrap destroys. | Dependence-aware intervals everywhere (R1) |

## The tests

---

### R1. Dependent data

**Principle.** The ordinary bootstrap treats observations as independent.
Resampling blocks of consecutive observations preserves dependence such as
volatility clustering (Künsch, 1989).

**Objective.** Check that every interval and p-value in the validation
respects the dependence in the data.

**Client harm.** Risk bands and claims rest on intervals that are too narrow,
so they fail more often than the stated confidence implies.

**Why existing tests miss it.** Standard routines assume independent
observations, and nothing visibly breaks when that assumption fails.

**Data.** The time series or clustered data behind each interval.

**Method.**
1. For each interval, identify the dependence: time (days, months) or
   clusters (clients sharing a relationship manager, campaign or household).
2. Use block resampling for time and cluster resampling for groups.
3. Where possible, check coverage by simulation.

**Setting the pass criteria.** All reported intervals use a method suited to
the dependence. Where coverage is known to fall short, the limitation is
stated beside the interval.

**What the illustration shows.** Across 200 simulated five-year histories,
95% intervals for volatility from single-day resampling contain the true
value only 68% of the time. Blocks of 63 days raise this to 78%. That is
better, but still short: a five-year history may hold no crisis, or one long
one, and no resampling scheme recovers what the history does not contain.
[`r1_dependent_data.py`](../05-illustrations/r1_dependent_data.py)

**Adjacent tests.** P2 and P5 use block intervals for this reason.
**Regulatory hook.** SR 11-7. **NIST AI RMF.** MEASURE 2.5.

---

### R2. Writing down which shifts matter

**Objective, method and pass criteria.** Draw the causal diagram of the
model's inputs and outcome, and mark which relationships may change between
environments: market regime, client acquisition channel, product range, the
model's own influence. Pass if a reviewed diagram exists and outputs are
shown to be stable on data spanning the identified shifts.

**Client harm.** No one can say in advance which change would break the
model, so the first sign is client harm.

**Regulatory hook.** SR 11-7 (conceptual soundness). **NIST AI RMF.** MAP 2.3.

### R3. Transfer to a new environment

**Objective, method and pass criteria.** Evaluate the model separately in
each environment it is used in (for example, a new channel, country or
client segment). Pass if the gap from the validated environment is within
tolerance.

**Client harm.** Clients in a newly added channel are served by a model
validated on a different population. D3 detects the input shift; R3 tests
the consequences.

**Regulatory hook.** Duty of care. **NIST AI RMF.** MEASURE 2.3.

### R4. Feedback loops

**Objective, method and pass criteria.** Track recommendation and acceptance
rates by group and asset class across model versions, looking for
self-reinforcing trends. For example, a portfolio recommended more often
becomes more common in the data, so the next model recommends it more. Pass
if no trend is unexplained.

**Client harm.** The model narrows towards its own past choices, including
any conflict (C1), rather than towards clients' interests.

**Regulatory hook.** Duty of loyalty (conflicts). **NIST AI RMF.** MEASURE 3.1.

### R5. Wrong model shape

**Objective, method and pass criteria.** Compare the model with a flexible
challenger region by region of the input space, to find where its assumed
form (linear, monotone, additive) is wrong. Pass if no region shows
misspecification beyond tolerance.

**Client harm.** The model is right on average and wrong for a particular
kind of client, for example those near retirement whose tolerance changes
non-linearly with age.

**Regulatory hook.** SR 11-7 (conceptual soundness). **NIST AI RMF.** MEASURE 2.5.

## How the tests fit together

R1 keeps the validation's own statistics honest. R2 is the plan, written
before the model goes live; R3 and R5 test it; R4 watches for the model
changing its own world.
