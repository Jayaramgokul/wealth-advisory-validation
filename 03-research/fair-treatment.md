# Fair treatment of clients

> Public sources only; full references in [SOURCES.md](../SOURCES.md). Every
> number quoted below comes from the simulated data in
> [05-illustrations](../05-illustrations/), not from any real firm.

## Why this lens

An adviser's duty of loyalty includes not unfairly favouring one client over
another (SEC Release IA-5248). A scoring or placement model applies the same logic to
everyone, which can look like a guarantee of fairness. It is not. The same
logic can rely on an input that stands in for a protected characteristic,
measure some clients less accurately than others, or serve one combination of
clients badly while every average looks fine. NIST AI RMF MEASURE 2.11 asks
for fairness and bias to be evaluated and the results documented, but it does
not say how.

The research below supplies the how. It also makes a second point that shaped
these tests: **a fairness test can itself be badly designed.** Groups picked
after seeing the data, samples too small to detect anything, or gaps reported
without context can each produce a misleading pass or a misleading fail.

## What I read, and what each source changed

| Source | The idea I took from it | What it changed in the tests |
|---|---|---|
| Kusner et al. (2017), *Counterfactual Fairness* | A decision is fair to an individual if it would be the same had their protected attribute been different. | Twin clients that differ in one attribute only (F1) |
| EEOC et al. (1978), *Uniform Guidelines*, 29 CFR 1607.4(D) | The four-fifths rule is a screen. The same section warns that small numbers can make large differences meaningless, and that statistical significance matters. | Four-fifths paired with a significance test and a power check (F2) |
| Buolamwini & Gebru (2018), *Gender Shades* | Commercial classifiers looked accurate overall but erred far more for one intersectional group. | Intersectional cells, with the worst group reported beside the average (F3, G1) |
| Barocas et al. (2021), *Designing Disaggregated Evaluations* | Choices about which groups, which metrics, what to adjust for, and how to handle uncertainty decide what an evaluation can show. | Raw and adjusted disparity side by side (F4); pre-registered groups; multiple-testing control (F3, S2) |
| Grable & Lytton (1999), *Financial Risk Tolerance Revisited*; Cronbach (1951) | A risk-tolerance questionnaire is a measurement instrument, and its reliability can be tested. | Reliability of the questionnaire by client group (F5) |
| Wilson (1927); Benjamini & Hochberg (1995) | Honest intervals for proportions, including small ones; controlling false discoveries when many groups are compared. | Used throughout F1 to F3 |

The four-fifths rule comes from employment law, not investment regulation. I
use it as a widely understood screening threshold, not as a legal standard
for advisers.

## The tests

Pass criteria are written as *how to set them*. For fairness the groups,
control factors and thresholds are fixed **before** the data is examined.
Anything chosen afterwards is labelled exploratory (F7).

---

### F1. Counterfactual twin clients

**Principle.** If changing only a client's protected attribute changes the
recommendation, that attribute is affecting the advice directly (Kusner et
al., 2017).

**Objective.** Show, without needing to see the model's internals, whether
any attribute that should not matter changes the recommendation.

**Client harm.** Two clients with identical answers receive different
portfolios because of where they live, or their sex.

**Why existing tests miss it.** Reviews check which inputs the model is
*documented* to use. A twin test checks what the model actually does,
including proxies such as region that nobody listed as protected.

**Data.** Client records, or realistic synthetic personas, and the ability to
call the scoring model.

**Method.**
1. For each client, create twins that differ only in one attribute (each value
   of sex, each region), with every questionnaire answer unchanged.
2. Run the model on each twin.
3. Count how often the recommended bucket changes, with a Wilson interval.

**Setting the pass criteria.** For a protected attribute, the expected rate is
zero. Agree a tolerance only if the model has a documented random element. For
an attribute that is a legitimate suitability factor, the change must match
the documented rule.

**What the illustration shows.** Two stand-in scoring rules are tested. The
one using only answers changes nothing. The one with a hidden regional
adjustment changes the recommendation for 12% to 29% of clients, depending on
the region assigned. Sex changes nothing in either.
[`f1_counterfactual_twins.py`](../05-illustrations/f1_counterfactual_twins.py)

**Limitation, stated plainly.** Flipping one attribute while holding the rest
fixed only catches *direct* use. Full counterfactual fairness also follows
the attribute's influence through other inputs that depend on it, which needs
a causal model. That is why F2 to F4 look at outcomes as well.

**Adjacent tests.** F4 checks for indirect effects through outcomes; O1
checks whether any single input dominates.
**Regulatory hook.** Duty of loyalty, not unfairly favouring one client over
another (IA-5248).
**NIST AI RMF.** MEASURE 2.11.

---

### F2. Adverse impact with honest statistics

**Principle.** A group whose favourable-outcome rate is below four-fifths of
the best group's rate is flagged as possible adverse impact. The Uniform
Guidelines themselves say small differences can matter where significant, and
large ones may not where numbers are small.

**Objective.** Screen every pre-agreed group for adverse impact, test whether
the differences are real, and say which groups are too small to judge.

**Client harm.** A group is quietly given less access to growth portfolios.
Or a small group is reported as treated fairly when the test had no chance of
detecting a problem.

**Why existing tests miss it.** A ratio on its own produces both errors. It
flags noise in small groups and passes them when they are too small to fail.

**Data.** Outcome per client (for example, access to a growth portfolio) and
group membership.

**Method.**
1. Outcome rate per group with a Wilson interval.
2. Impact ratio against the best-treated group.
3. Chi-square test of equal rates across groups.
4. For each group, the smallest gap the test could reliably detect (80%
   power). If it is larger than the gap that would matter, the group is
   **inconclusive**, not passing.

**Setting the pass criteria.** Pass if no group is below four-fifths with
statistical support. Agree in advance the gap that would matter (here, 10
points); any group whose detectable gap exceeds it is reported as
inconclusive.

**What the illustration shows.** Group D has an impact ratio of 0.75 and the
chi-square test confirms the rates differ. Group E, with 60 clients, has an
impact ratio of 0.91 and would "pass", but a gap as large as 18 points could
go undetected, so it is reported as inconclusive.
[`f2_adverse_impact_four_fifths.py`](../05-illustrations/f2_adverse_impact_four_fifths.py)

**Adjacent tests.** F3 extends this to combinations of factors; F4 asks
whether a gap is explained by legitimate factors.
**Regulatory hook.** Duty of loyalty (IA-5248).
**NIST AI RMF.** MEASURE 2.11.

---

### F3. Intersectional disaggregation, with the worst group as co-headline

**Principle.** Gender Shades found commercial classifiers with low error
overall and very high error for one intersection of skin type and gender.
Single-factor checks could not have found it.

**Objective.** Find any combination of client characteristics that is badly
served, and report it beside the average.

**Client harm.** Older, inexperienced clients with small accounts are
misplaced far more often than anyone else, while every summary figure looks
healthy.

**Why existing tests miss it.** Fairness reviews commonly check one factor at
a time. Each factor alone can show only a small gap.

**Data.** Outcome per client (here, whether the placement was suitable) and a
small, pre-agreed set of factors.

**Method.**
1. Pre-register a limited grid of factor combinations. A grid that is too
   fine produces empty or tiny cells.
2. Outcome rate per cell with a Wilson interval; cells below a minimum size
   are listed as too small to judge.
3. Test each cell against the rest and control the false discovery rate
   (Benjamini-Hochberg), because many cells are being compared.
4. Report the worst adequately sized cell beside the overall rate (G1).

**Setting the pass criteria.** Every populated cell is within the agreed
tolerance of the overall rate, or has a remediation plan. Agree the grid,
minimum cell size and tolerance before looking.

**What the illustration shows.** Single factors show gaps of 3 to 8 points.
The worst cell (65+, novice, small account) is suitably placed 62% of the
time against 79% overall, and survives the correction for multiple testing.
[`f3_worst_group_intersectional.py`](../05-illustrations/f3_worst_group_intersectional.py)

**Adjacent tests.** G1 makes the worst group a standing part of every report;
G2 asks which direction the errors lean; P4 covers the retirement-specific
risk for older clients.
**Regulatory hook.** Duty of care and loyalty (IA-5248); senior investors
(FINRA Rule 2165).
**NIST AI RMF.** MEASURE 2.11.

---

### F4. Raw and adjusted disparity, side by side

**Principle.** A raw gap between groups can be explained by legitimate
factors, or it can hide part of a real gap. Barocas et al. recommend
conditional analysis with the control factors chosen in advance.

**Objective.** Show how much of a difference between groups remains once
legitimate suitability factors are accounted for.

**Client harm.** Either a legitimate difference is treated as unfair and
"corrected", harming suitability, or an unfair difference is waved away as
explained.

**Why existing tests miss it.** A single disparity figure cannot distinguish
these cases, whichever version is reported.

**Data.** Score or outcome per client, group membership, and the agreed
legitimate factors (here, measured risk tolerance).

**Method.**
1. Regress the outcome on group alone: the raw gap.
2. Regress it on group plus the agreed legitimate factors: the adjusted gap,
   with its interval.
3. Report both, together with the list of control factors.

**Setting the pass criteria.** The adjusted gap's interval lies within the
agreed tolerance. Control factors are agreed with compliance in advance,
because each one is a statement that a difference is legitimate.

**What the illustration shows.** In two simulated scenarios the raw gaps are
similar in direction (−6.2 and −10.2 points). After adjusting for tolerance,
the first falls to +0.1 (interval −0.2 to +0.4): explained. The second
remains at −3.9 (interval −4.2 to −3.6): not explained.
[`f4_adjusted_disparity.py`](../05-illustrations/f4_adjusted_disparity.py)

**Caution.** Adjusting for a factor that is itself affected by the protected
attribute can hide a real disparity. This is why the control list needs
justifying, not just choosing.

**Adjacent tests.** F1 (direct effect); F6 (which stage of the pipeline
introduces the gap).
**Regulatory hook.** Duty of loyalty (IA-5248).
**NIST AI RMF.** MEASURE 2.11.

---

### F5. Does the questionnaire measure every client equally well?

**Principle.** A risk-tolerance questionnaire is a measurement instrument
(Grable & Lytton, 1999). Its reliability, for example internal consistency
measured by Cronbach's alpha, can differ between groups.

**Objective.** Check whether the questionnaire measures risk tolerance as
reliably for each client group, for example novice and experienced investors.

**Client harm.** Clients the questionnaire measures poorly are more often
placed in the wrong portfolio. Every fairness test that uses the score as its
yardstick inherits the error.

**Why existing tests miss it.** Questionnaires are usually reviewed for
wording and scoring logic, not tested statistically by group.

**Data.** Item-level questionnaire answers by client group; where available,
an independent measure of tolerance or test-retest answers.

**Method.**
1. Cronbach's alpha per group, with a bootstrap interval.
2. Where possible, correlation of the score with an independent measure.
3. Compare across groups.

**Setting the pass criteria.** Agree a minimum reliability and a maximum gap
between groups. Where a group falls short, remedies include clearer items,
follow-up questions when answers contradict each other (as the SEC's
2017 guidance suggests), or disclosing the limitation.

**What the illustration shows.** Alpha is 0.84 for experienced investors and
0.54 for novices, with intervals that do not overlap. The score also tracks
true tolerance less closely for novices (correlation 0.74 against 0.91).
[`f5_questionnaire_reliability.py`](../05-illustrations/f5_questionnaire_reliability.py)

**Adjacent tests.** U2 (refer borderline clients to a human), which is most
needed where measurement is weakest; F3 (novices appear in the worst cell).
**Regulatory hook.** Questionnaire design (SEC IM Guidance 2017-02); duty of
care, reasonable inquiry into the client's risk tolerance (IA-5248).
**NIST AI RMF.** MEASURE 2.11; MEASURE 2.1 (evaluation data and measurement documented).

---

## Designing the fairness evaluation itself

Barocas et al.'s main point is that a disaggregated evaluation is a set of
design choices, and each choice can quietly decide the result. F6 to F10 turn
those choices into checks on the evaluation process. They are about process,
so their entries are shorter.

### F6. Where in the pipeline does unfairness arise

**Objective, method and pass criteria.** Measure the same fairness metric
after each stage: questionnaire answers, risk score, bucket, portfolio,
explanation. Pass if each disparity found by F2 to F4 is traced to the stage
that introduces it.
**Client harm.** A disparity is found but fixed in the wrong place, for
example by adjusting the portfolio when the questionnaire is the cause (F5).
**Regulatory hook.** SR 11-7 (effective challenge). **NIST AI RMF.** MEASURE 2.11.

### F7. Confirmatory or exploratory

**Objective, method and pass criteria.** Label every fairness result as
confirmatory (a hypothesis, groups and threshold written down and dated
before the data was seen) or exploratory (found while looking). Pass if every
result carries a label and every confirmatory claim has its dated record.
**Client harm.** Groups chosen after seeing the data turn noise into
findings, or real problems into passes.
**Regulatory hook.** SR 11-7 (documentation). **NIST AI RMF.** MEASURE 2.13. Related: S2.

### F8. Is the evaluation data fit for purpose

**Objective, method and pass criteria.** Write a datasheet (Gebru et al.)
for each dataset used in the fairness evaluation, and compare its group
composition with the live client base. Pass if datasheets exist and gaps are
stated beside the results.
**Client harm.** Fairness conclusions rest on data with too few members of
some groups, or of unknown origin.
**Regulatory hook.** SR 11-7 (data). **NIST AI RMF.** MEASURE 2.1. Related: G5, D7.

### F9. Fairness on real usage

**Objective, method and pass criteria.** Repeat the disaggregated evaluation
periodically on consented production data and reconcile it with the
validation results. Pass if it runs on schedule and differences are
explained.
**Client harm.** Synthetic personas miss how real clients answer and
interact.
**Regulatory hook.** Duty of care (monitoring). **NIST AI RMF.** MEASURE 2.3.

### F10. When to bring in outside review

**Objective, method and pass criteria.** Agree written triggers for an
independent outside review (for example, a confirmed F2 finding, a new client
segment, a material model change). Pass if the triggers are documented and
followed.
**Client harm.** Internal evaluators share the blind spots of the team that
built the model.
**Regulatory hook.** SR 11-7 (independence). **NIST AI RMF.** MEASURE 1.3.

## How the tests fit together

F5 checks the ruler. F1 checks for direct use of an attribute. F2 screens
outcomes by group honestly. F3 looks where single factors cannot. F4 separates
legitimate from unexplained differences. Run in that order, a finding in one
usually explains a finding in another: in the illustrations, the group the
questionnaire measures worst (novices) is also in the worst intersectional
cell. F6 to F10 make sure the evaluation producing these results is itself
sound: traced to its source, honestly labelled, run on fit data, repeated in
production, and open to outside challenge.
