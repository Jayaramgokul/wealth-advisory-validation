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

**Objective.** Make the worst-served group a standing part of every report,
so that no aggregate figure reaches a decision-maker without it.

**Client harm.** A committee approves a model on an 80% suitability rate
without seeing that one group sits near 60%.

**Why existing tests miss it.** Disaggregated analysis is often done once,
during validation, and then dropped from the regular reports that governance
committees and senior management actually read.

**Data.** The same per-client outcomes and characteristics used in F3, for
every reporting period.

**Method.**
1. Run the F3 breakdown each period, with the same pre-agreed grid and
   minimum cell size.
2. Next to every aggregate figure, show the worst cell large enough to judge,
   its interval, and the gap to the aggregate.
3. Track the worst cell over time, including whether it is the same group
   each period. A worst group that keeps recurring is a structural problem,
   not noise.

**Setting the pass criteria.** Pass if every report to governance carries the
worst group beside the aggregate, in the agreed format. A report without it
is incomplete, whatever its figures show. The gap itself is judged by F3's
tolerance.

**What the illustration shows.** Built into
[F3](fair-treatment.md#f3-intersectional-disaggregation-with-the-worst-group-as-co-headline):
the overall suitability rate is 79%, and the worst group, older novices with
small accounts, is at 62% (interval 57–67%). Reported alone, the 79% would
have looked healthy.
[`f3_worst_group_intersectional.py`](../05-illustrations/f3_worst_group_intersectional.py)

**Adjacent tests.**
- **F3** finds the worst group; G1 keeps it in view.
- **G4** sets the reporting standard that G1 is part of.

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

**Data.** For each client: the band the model placed them in, the band that
was actually suitable, and their group. The suitable band needs an agreed
reference, such as an adviser's file review or a fuller assessment of the
client. D7 covers how reliable those reference labels are, because errors in
the reference look like errors in the model.

**Method.**
1. **Classify every placement** as correct, too aggressive (a higher-risk
   band than suitable) or too cautious (a lower one).
2. **Rates per group,** for each direction separately, with 95% Wilson
   intervals.
3. **A chi-square test** on the table of aggressive and cautious errors by
   group, which asks whether the split between directions differs across
   groups.
4. **Look at the size of the miss** as well as its direction: a placement two
   bands too high is a worse error than one band.

**Setting the pass criteria.** Agree a tolerance for how far one group's
errors may lean in either direction, judged on intervals, not point
estimates. Because U1 shows that an aggressive error usually costs a client
more than a cautious one, the tolerance for over-placement is normally
tighter. A group that fails is a finding even if its overall error rate is
in line with everyone else's.

**What the illustration shows.** The script simulates 6,000 clients in four
regions, and a placement model whose error leans by region: 4 points too
high for the north, 4 points too low for the south, and unbiased elsewhere.
This is the kind of pattern a regional input standing in for something the
model should not use would create.

| Region | Misplaced | Too aggressive (95% interval) | Too cautious (95% interval) |
|---|---|---|---|
| East | 29% | 14% (12–15%) | 16% (14–17%) |
| North | 35% | **29%** (27–32%) | 6% (5–7%) |
| South | 39% | 5% (4–6%) | **34%** (32–37%) |
| West | 29% | 14% (13–16%) | 15% (13–17%) |

North and south have similar overall error rates, so a check on error rates
would treat them alike. Split by direction, north's clients are pushed into
too much risk and south's into too little: opposite harms, needing opposite
fixes. The chi-square test confirms the split differs across regions (p ≈
10⁻¹²²).
[`g2_direction_of_errors.py`](../05-illustrations/g2_direction_of_errors.py)

**Adjacent tests.**
- **U1** puts a cost on each direction of error, so they can be weighed.
- **F1** would find the regional input directly, by flipping region on twin
  clients.
- **F3** shows which combinations of clients are misplaced most; G2 shows
  which way.

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

**Data.**
- **The model's score for each client,** before any cut-off is applied.
- **Whether each client is truly suitable** for the outcome the cut-off
  controls, from the same reference as G2.
- **Group membership,** for the groups that matter for this decision.
- **Every cut-off the model uses,** with the reason it was set where it is.

**Method.**
1. **Sweep the cut-off** across a plausible range around its current value.
2. **For each value and each group,** compute the share of clients for whom
   the outcome is *not* suitable who receive it anyway. Where the opposite
   error matters too, compute the share of suitable clients denied it.
3. **Plot one curve per group,** and mark the chosen value.
4. **Note where the curves cross.** On one side of the crossing, one group
   bears more of the cost; on the other side, the other group does.

**Setting the pass criteria.** The chosen threshold is justified against its
effect on each group, not only against overall error, and the justification
is documented. Where the threshold sits near a crossing point, a small
recalibration can move the cost from one group to another, so the
justification should say which way it falls and why that is acceptable.

**What the illustration shows.** The script simulates 20,000 clients and asks
who is offered the highest-risk band (Band 5) when it is not suitable for
them. Band 5 is treated as suitable for clients whose true tolerance is 75
or more. Novices answer the questionnaire less consistently than experienced
investors (F5).

| Cut-off | Novices offered Band 5 when unsuitable | Experienced clients offered it when unsuitable |
|---|---|---|
| 65 | 25.8% | 41.5% |
| 70 | 14.3% | 22.0% |
| 75 | 9.6% | 13.8% |
| 80 | 3.4% | 3.6% |
| 85 | 0.7% | 0.3% |

At low cut-offs, experienced clients bear more of the cost, because many of
them sit just below the suitability line. From a cut-off of about 82 upwards,
the order reverses: novices bear more, because their noisier answers push a
few far above their true tolerance. The same model gives a different answer
to "who pays for this threshold" depending only on where the line is drawn.
[`g3_threshold_sweep.py`](../05-illustrations/g3_threshold_sweep.py)

**Adjacent tests.**
- **U2** uses a threshold to decide when to refer a client to a human; G3's
  sweep applies to that threshold too.
- **F5** explains why novices' scores are noisier.
- **U1** gives the cost of each error, which turns the curves into a single
  cost per threshold and group.

**Regulatory hook.** Duty of care. **NIST AI RMF.** MEASURE 2.11.

---

### G4. Disaggregated reporting standard

**Objective.** Fix a minimum breakdown that every metric reported to
governance or clients must carry.

**Client harm.** Aggregates reach decision-makers without the breakdown that
would show who is badly served.

**Why existing tests miss it.** Breakdowns depend on whoever writes each
report, so they vary from report to report and disappear under time
pressure.

**Data.** The list of recurring reports to governance committees, senior
management and clients, and the metrics each one contains.

**Method.**
1. **Write the standard:** the characteristics every metric is broken down
   by (for example, age band, account size, region and experience), the
   minimum cell size, and the format (worst group beside the aggregate, as in
   G1).
2. **Agree it** with the model owner, compliance and the committees that
   receive the reports.
3. **Audit** a sample of reports each period against the standard.

**Setting the pass criteria.** Pass if periodic audits find the standard
followed in every sampled report, and any departure is explained.

**Adjacent tests.**
- **G1** is the most important element of the standard.
- **F7** keeps breakdowns chosen in advance separate from ones added after
  seeing results.

**Regulatory hook.** Disclosure; SR 26-2. **NIST AI RMF.** MEASURE 2.8.

### G5. Benchmark composition

**Principle.** Gender Shades built a new benchmark because existing ones
under-represented the groups being judged.

**Objective.** Check that the data used to validate the model contains each
client group in proportions close to the live client base.

**Client harm.** Validation results do not transfer to the clients actually
served.

**Why existing tests miss it.** Validation samples are often drawn for
convenience, such as a recent period or one channel, and their make-up is
rarely compared with the client base.

**Data.** Group counts in each validation dataset, and in the live client
base for the same period.

**Method.**
1. **Compare each group's share** in the validation data with its share in
   the live client base.
2. **Flag groups** that are under-represented beyond the agreed tolerance,
   or so small that their results will be inconclusive (the power check in
   F2).
3. **Document small cells** by name, with what would make them testable:
   targeted sampling, a longer period, or synthetic cases clearly labelled as
   such.

**Setting the pass criteria.** Pass if every group's share is within the
agreed tolerance of the client base, and every small cell is documented
beside the results it affects.

**Adjacent tests.**
- **F8** applies the same check to the data used for fairness testing.
- **D3** watches for the client base itself drifting away from the
  validation data over time.

**Regulatory hook.** SR 26-2 (data selection, under conceptual soundness). **NIST AI RMF.** MEASURE 2.3.

### G6. Disparities without demographic data

**Principle.** Many firms do not collect protected attributes; Barocas et al.
discuss the trade-offs of working without them.

**Objective.** Look for disparities in groups the firm does not record, using
proxies that have been reviewed and whose errors are known.

**Client harm.** The firm cannot see disparities it has no data on, and so
assumes there are none.

**Why existing tests miss it.** When a characteristic is not recorded,
fairness testing on it is usually skipped rather than approached another
way.

**Data.** The observable information the firm holds that correlates with the
missing characteristic, such as geography, and, where it exists, a sample in
which the characteristic is known, to measure how accurate the proxy is.

**Method.**
1. **Choose proxies with legal review,** documenting why each is acceptable
   and what it cannot show.
2. **Measure each proxy's error** where possible: how often it assigns the
   wrong group, and whether that error differs between groups.
3. **Run the F2 to F4 tests on proxy-defined groups,** and widen the
   uncertainty to allow for the proxy's error.
4. **Report results as indicative,** with the proxy and its known error
   stated beside them.

**Setting the pass criteria.** Pass if a reviewed proxy map exists, is
tested routinely, and every result based on it carries its limitation.

**Adjacent tests.**
- **F8** documents how group membership was obtained for each dataset.
- **F1** can test whether the proxy itself, such as region, changes the
  model's recommendation directly.

**Regulatory hook.** Fair treatment. **NIST AI RMF.** MEASURE 2.11.

## How the tests fit together

G1 makes the worst group visible; G2 shows which way it is harmed; G3 shows
whether a design choice caused it. G4 to G6 make sure the breakdowns happen at
all, on data that represents the clients, even when protected attributes are
not collected.
