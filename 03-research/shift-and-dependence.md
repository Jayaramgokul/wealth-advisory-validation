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

**Data.** The data behind every interval and p-value in the validation,
with enough structure kept to see how observations are related:
- **dates,** for market and portfolio returns, where volatile days cluster;
- **groupings,** for client data: clients who share a relationship manager,
  joined through the same campaign, or belong to the same household tend to
  resemble each other.

**Method.**
1. **Identify the dependence** behind each interval: in time (consecutive
   days or months) or in clusters (groups of related clients).
2. **Choose a resampling scheme that keeps it.** For time series, resample
   blocks of consecutive observations, long enough to contain a typical
   volatile spell. For clusters, resample whole clusters rather than
   individual clients.
3. **Check coverage by simulation** where possible: generate many histories
   from a model with known truth, build an interval from each, and count how
   often the intervals contain the truth. A 95% interval should do so about
   95% of the time.
4. **Try a few block lengths.** If the interval changes a lot with the block
   length, the history is probably too short to pin the figure down.

**Setting the pass criteria.** Pass if every reported interval uses a method
suited to the dependence in its data. Where coverage is known to fall short,
the shortfall is stated beside the interval, so readers do not take a nominal
95% at face value.

**What the illustration shows.** The script generates 200 independent
five-year histories of the 50/50 portfolio from the simulated market, whose
true long-run volatility is 9.8%. From each history it builds a 95% interval
for volatility two ways.

| Resampling | Intervals that contain the true value | Average width |
|---|---|---|
| Single days, one at a time | 68% | 3.1 points |
| Blocks of 63 days (about three months) | 78% | 4.0 points |
| What a 95% interval promises | 95% | |

Single-day resampling treats calm and crisis days as interchangeable, so its
intervals are too narrow and miss the truth almost a third of the time.
Blocks keep volatile spells together, widen the intervals and do better. They
still fall short, because a five-year history may contain no crisis at all,
or one long one, and no resampling scheme can recover what the history does
not contain. The honest report states that shortfall.
[`r1_dependent_data.py`](../05-illustrations/r1_dependent_data.py)

**Adjacent tests.**
- **P2** and **P5** use block intervals for this reason.
- **D4** addresses what the history does not contain, by stressing it
  directly.
- **S2** relies on p-values that are only valid if dependence is handled.

**Regulatory hook.** SR 26-2. **NIST AI RMF.** MEASURE 2.5.

---

### R2. Writing down which shifts matter

**Objective.** Write down, before the model goes live, which changes in the
world could break it, and show that it holds up across the changes already
seen.

**Client harm.** No one can say in advance which change would break the
model, so the first sign is client harm.

**Why existing tests miss it.** Validation tests the model on data like the
data it was built on. Which changes would matter is left to whoever notices
a problem later.

**Data.** The model's inputs, outcome and documented assumptions, and data
spanning as many different conditions as possible: market regimes, client
acquisition channels, product ranges, and periods before and after past
model changes.

**Method.**
1. **Draw a causal diagram** of the inputs and the outcome: which factors
   influence which, as the model owner and validator understand them.
2. **Mark which relationships could change** between environments, such as:
   - market regime (D4 shows one example);
   - the channel clients arrive through (D3);
   - the products on offer;
   - the model's own influence on the data it later learns from (R4).
3. **Have the diagram reviewed** by people who know the business and the
   clients, not only the model.
4. **Test stability on data that spans each identified shift,** for example
   comparing performance in calm and stressed periods, or across channels.
5. **Turn each identified shift into a monitoring item** for D3.

**Setting the pass criteria.** Pass if a reviewed diagram exists, every
marked relationship has a test or a monitoring item, and outputs are shown
to be stable, within tolerance, on data spanning the identified shifts.

**Adjacent tests.**
- **D3** monitors the shifts this test identifies.
- **R3** tests the model in each new environment.

**Regulatory hook.** SR 26-2 (conceptual soundness). **NIST AI RMF.** MAP 2.3.

### R3. Transfer to a new environment

**Objective.** Test the model separately in each environment it is used in,
before relying on it there.

**Client harm.** Clients in a newly added channel are served by a model
validated on a different population. D3 detects the input shift; R3 tests
the consequences.

**Why existing tests miss it.** A model approved for one population is often
extended to others, such as a new channel, country or client segment, on
the strength of its original validation.

**Data.** Outcomes and reference labels for clients in each environment,
separately: the original one, and each one the model has been extended to.

**Method.**
1. **Evaluate the model in each environment** with the same measures used in
   the original validation: expected cost (U1), errors by direction (G2),
   fairness by group (F2 to F4).
2. **Compare with the validated environment,** with intervals, since a new
   environment usually starts with few clients.
3. **Look for reasons** for any gap: different clients, different products,
   different data recording, or a different relationship between inputs and
   outcome.

**Setting the pass criteria.** Agree a tolerance for the gap from the
validated environment. Pass if every environment is within it, or the gap is
explained and the model adjusted. Where a new environment has too few
clients to judge, the model is used there only with extra controls, such as
more referrals to a human (U2), until it can be judged.

**Adjacent tests.**
- **D3** detects that the population has changed.
- **G5** checks that the validation data represents each environment.

**Regulatory hook.** Duty of care. **NIST AI RMF.** MEASURE 2.3.

### R4. Feedback loops

**Objective.** Detect when the model's own recommendations start shaping the
data it is later retrained on.

**Client harm.** The model narrows towards its own past choices, including
any conflict (C1), rather than towards clients' interests.

**Why existing tests miss it.** Each model version is validated on its own,
so a trend that builds up across versions is never seen.

**Data.** Recommendation and acceptance rates, by client group and asset
class, for every model version, and the data each version was trained on.

**Method.**
1. **Track recommendation and acceptance rates** across model versions, by
   group and by asset class.
2. **Look for self-reinforcing trends.** For example, a portfolio recommended
   more often becomes more common in the data, so the next model recommends
   it more.
3. **Check what the model learns from.** If it learns from what clients
   accepted, it partly learns from its own past advice. A held-back sample of
   clients advised by a fixed rule, or reviewed by a human, gives an
   independent reference.
4. **Compare with a neutral benchmark** for the same clients, as in C1.

**Setting the pass criteria.** Pass if no trend across versions is
unexplained, and the training data includes an independent reference that
the model's own advice did not shape.

**Adjacent tests.**
- **C1** compares recommendations with a neutral benchmark at one point in
  time; R4 watches the trend across versions.
- **O2** keeps a challenger running, which also gives an outside reference.

**Regulatory hook.** Duty of loyalty (conflicts). **NIST AI RMF.** MEASURE 3.1.

### R5. Wrong model shape

**Objective.** Find the kinds of client for whom the model's assumed form,
such as linear, monotone or additive, is wrong.

**Client harm.** The model is right on average and wrong for a particular
kind of client, for example those near retirement whose tolerance changes
non-linearly with age.

**Why existing tests miss it.** Overall fit measures average over all
clients, so a region where the model's shape is wrong can hide among the
regions where it is right.

**Data.** The model's inputs, predictions and reference outcomes on held-out
clients.

**Method.**
1. **Fit a flexible challenger** on the same data, such as gradient-boosted
   trees, which can follow curves and interactions the model cannot.
2. **Compare the two region by region** across the inputs: for example by age
   band, wealth band and horizon, or by the challenger's own splits.
3. **Look where they disagree most,** and check those regions against the
   reference outcomes: if the challenger is right there, the model's shape is
   wrong for those clients.
4. **Plot the outcome against each key input,** with both models' fits, to
   show the shape of the miss.

**Setting the pass criteria.** Agree a tolerance for the difference between
the model and the reference outcome in any region large enough to judge.
Pass if no region exceeds it, or the shape is corrected for the regions that
do.

**Adjacent tests.**
- **O2** and **O3** use challengers more generally; R5 uses one to find where
  the model's shape is wrong.
- **F3** looks for badly served combinations of client characteristics; R5
  looks for badly fitted regions of the inputs.

**Regulatory hook.** SR 26-2 (conceptual soundness). **NIST AI RMF.** MEASURE 2.5.

## How the tests fit together

R1 keeps the validation's own statistics honest. R2 is the plan, written
before the model goes live; R3 and R5 test it; R4 watches for the model
changing its own world.
