# Groups an average can hide

> Public sources only; full references in [SOURCES.md](../SOURCES.md). Every
> number quoted below comes from the simulated data in
> [05-illustrations](../05-illustrations/), not from any real firm.

## Why this lens

*Gender Shades* (Buolamwini & Gebru, 2018) audited commercial gender
classifiers that looked highly accurate overall. Broken down by skin type and
gender together, error rates reached 34.7% for darker-skinned women against
at most 0.8% for lighter-skinned men. Nothing in the aggregate figures hinted
at it.

The fair-treatment tests (F1 to F5) ask whether clients are treated alike. This
lens asks a related but separate question about **reporting**: does the way
results are summarised let a badly served group, a one-sided pattern of
errors, or a threshold's uneven cost go unseen?

## What I read, and what each source changed

| Source | The idea I took from it | What it changed in the tests |
|---|---|---|
| Buolamwini & Gebru (2018), *Gender Shades* | Intersections reveal what single factors hide; benchmarks must contain the groups being judged. | Worst group as co-headline (G1); benchmark composition (G5) |
| Barocas et al. (2021), *Designing Disaggregated Evaluations* | The choice of metric, threshold and grouping decides what a disaggregated evaluation can show. | Direction of errors (G2); threshold sweeps (G3); a written reporting standard (G4) |
| Barocas et al. (2021), on missing demographic data | Firms often lack protected attributes and need careful, reviewed alternatives. | Disparities without demographic data (G6) |

## The tests

---

### G1. Worst group as co-headline

Built into [F3](fair-treatment.md#f3-intersectional-disaggregation-with-the-worst-group-as-co-headline):
every aggregate figure is reported with its worst adequately sized group and
the gap beside it. In the F3 illustration the overall suitability rate is 79%
and the worst group's is 62%.
[`f3_worst_group_intersectional.py`](../05-illustrations/f3_worst_group_intersectional.py)
**NIST AI RMF.** MEASURE 2.11.

---

### G2. Direction of errors by group

**Principle.** Two groups can have the same error rate but different kinds of
error. Barocas et al. stress choosing metrics that match the harm.

**Objective.** For each group, separate placements that are too aggressive
from placements that are too cautious.

**Client harm.** One group is pushed into more risk than it can bear, another
into too little. The harms differ and need different fixes.

**Why existing tests miss it.** Error rates by group, the usual disaggregated
metric, add the two directions together.

**Data.** True and placed buckets with group membership.

**Method.**
1. Over-placement and under-placement rates per group, with Wilson intervals.
2. A chi-square test of whether the split differs across groups.

**Setting the pass criteria.** No group's errors lean one way beyond an
agreed tolerance, judged on intervals, not point estimates.

**What the illustration shows.** North and south have similar error rates
(35% and 39%). But 29% of north's clients are placed too aggressively and 6%
too cautiously, while south's split is 5% and 34%. East and west are balanced.
[`g2_direction_of_errors.py`](../05-illustrations/g2_direction_of_errors.py)

**Adjacent tests.** U1 (asymmetric costs); F1 (region as a proxy).
**Regulatory hook.** Duty of care (suitability). **NIST AI RMF.** MEASURE 2.11.

---

### G3. Thresholds and who they affect

**Principle.** Any cut-off redistributes errors between groups whose scores
are distributed differently.

**Objective.** Show how the choice of each cut-off (between buckets, or
between answering and referring) changes outcomes for each group, so the
chosen value can be justified.

**Client harm.** A cut-off tuned on overall error quietly loads the cost onto
one group.

**Why existing tests miss it.** Thresholds are usually validated at the
chosen value only.

**Data.** Scores, true suitability and group membership.

**Method.**
1. Sweep the cut-off across a plausible range.
2. For each value and group, the share of clients for whom the outcome is
   unsuitable but who receive it anyway.
3. Plot the curves and mark the chosen value.

**Setting the pass criteria.** The chosen threshold is justified against its
effect on each group, and the justification is documented.

**What the illustration shows.** At low cut-offs, more unsuitable
*experienced* clients are offered the highest-risk band, because many sit
just below the suitability line (at 65: 42% against 26% for novices). From
about 82 upwards the order reverses, because novices' noisier answers push a
few far above their true tolerance. Which group bears the cost depends on
where the line is drawn.
[`g3_threshold_sweep.py`](../05-illustrations/g3_threshold_sweep.py)

**Regulatory hook.** Duty of care. **NIST AI RMF.** MEASURE 2.11.

---

### G4. Disaggregated reporting standard

**Objective, method and pass criteria.** Write down a minimum breakdown (for
example age band, account size, region and experience) for every metric
reported to governance or clients. Pass if periodic audits find it followed.

**Client harm.** Aggregates reach decision-makers without the breakdown that
would show who is badly served.

**Regulatory hook.** Disclosure; SR 26-2. **NIST AI RMF.** MEASURE 2.8.

### G5. Benchmark composition

**Principle.** Gender Shades built a new benchmark because existing ones
under-represented the groups being judged.

**Objective, method and pass criteria.** Compare group shares in the
validation data with the live client base. Pass if they match within
tolerance and small cells are documented as such.

**Client harm.** Validation results do not transfer to the clients actually
served.

**Regulatory hook.** SR 26-2 (data selection, under conceptual soundness). **NIST AI RMF.** MEASURE 2.3. Related: F8.

### G6. Disparities without demographic data

**Principle.** Many firms do not collect protected attributes; Barocas et al.
discuss the trade-offs of working without them.

**Objective, method and pass criteria.** Use legally reviewed observable
proxies (for example, geography) to look for disparities, documenting each
proxy's known error. Pass if a reviewed proxy map exists and is tested
routinely.

**Client harm.** The firm cannot see disparities it has no data on, and so
assumes there are none.

**Regulatory hook.** Fair treatment. **NIST AI RMF.** MEASURE 2.11.

## How the tests fit together

G1 makes the worst group visible; G2 shows which way it is harmed; G3 shows
whether a design choice caused it. G4 to G6 make sure the breakdowns happen at
all, on data that represents the clients, even when protected attributes are
not collected.
