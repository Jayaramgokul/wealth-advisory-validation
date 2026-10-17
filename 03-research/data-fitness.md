# The data underneath the model

> Public sources only; full references in [SOURCES.md](../SOURCES.md). Every
> number quoted below comes from the simulated data in
> [05-illustrations](../05-illustrations/), not from any real firm.

## Why this lens

Models used in advice learn from, are tested on, and are marketed with data:
market histories behind backtests, fund universes behind product choice,
client records behind the risk score, and reviewer labels behind "accuracy".
SR 26-2 includes an assessment of data quality and relevance in model testing, but in practice
that often means completeness checks and reconciliations. Those catch broken
data, not data that is quietly *unrepresentative*.

Gebru et al.'s *Datasheets for Datasets* gives a better set of questions:
why the data was collected, what it contains and leaves out, how and when it
was gathered, how it was labelled, and how it is maintained. I read each
question as a test: **if the honest answer were unflattering, what would go
wrong for the client, and how would we find out?**

## What I read, and what each source changed

| Source | The idea I took from it | What it changed in the tests |
|---|---|---|
| Gebru et al. (2021), *Datasheets for Datasets* | A fixed list of questions about motivation, composition, collection, labelling and maintenance exposes gaps that model metrics never show. | Each datasheet question became a candidate test (D1 to D7) |
| Elton, Gruber & Blake (1996), *Survivorship Bias and Mutual Fund Performance* | Funds that close are mostly poor performers; leaving them out flatters average returns by close to 1% a year. | Rebuild the universe as it existed at each date (D1) |
| Yurdakul (2018), *Statistical Properties of Population Stability Index* | PSI's behaviour depends on sample size and binning, so fixed thresholds like 0.10 and 0.25 are rules of thumb, not tests with known error rates. | Monitor inputs with PSI, but treat the bands as review triggers (D3) |
| DeMiguel, Garlappi & Uppal (2009), *Optimal Versus Naive Diversification* | Sophisticated allocation models often fail to beat a simple equal-weighted portfolio out of sample. | Any model must beat simple baselines by a margin that survives resampling (D6) |
| Cohen (1960, 1968), kappa and weighted kappa | Agreement between raters should be corrected for chance; for ordered categories, near misses can be weighted. | Reviewer labels are tested before they are used to judge the model (D7) |

## The tests

Tests with an illustration have a full entry. Tests that are mainly about
process have a shorter one.

---

### D1. Survivorship bias in backtest data

**Principle.** A datasheet asks what the data leaves out and why. A fund list
taken from today leaves out every fund that closed, and funds mostly close
because they did badly (Elton, Gruber & Blake, 1996).

**Objective.** Check that any backtest used in product design or shown to
clients is built on the universe that was investable at each date.

**Client harm.** Clients are shown, and choose on the basis of, a history
nobody could have achieved.

**Why existing tests miss it.** A review usually reproduces the backtest from
the firm's data. If the data starts from today's list, the reproduction
matches perfectly and inherits the bias.

**Data.** The fund or asset universe as it stood at each date, including
closed, merged and delisted products, and their returns up to closure.

**Method.**
1. Rebuild the universe point in time.
2. Re-run the backtest on the full universe, holding closed products until
   their closure date.
3. Compare with the published result.

**Setting the pass criteria.** Agree in advance how large a difference is
material for client communications (for example, a fraction of a percent a
year). The universe definition must be documented either way.

**What the illustration shows.** Of 400 simulated funds, 181 close over ten
years after trailing the market. A backtest on the survivors shows 8.9% a
year against 7.6% on the full universe: a bias of 1.3% a year, or 13% over
the decade.
[`d1_survivorship_bias.py`](../05-illustrations/d1_survivorship_bias.py)

**Regulatory hook.** Marketing Rule (hypothetical performance; fair and
balanced presentation). **NIST AI RMF.** MEASURE 2.5.

---

### D2. Look-ahead bias and label leakage

**Principle.** A datasheet asks when each piece of data was collected. A
backtest is only honest if every decision uses information that was
available at that moment.

**Objective.** Confirm that no feature, label or rebalancing signal uses
information from after the decision date.

**Client harm.** A strategy appears to manage risk or add return, and the
advantage disappears in live use, after clients have relied on it.

**Why existing tests miss it.** Leakage rarely shows up as an error. The code
runs, the numbers reconcile, and the backtest simply looks good.

**Data.** For each field: the date it refers to and the date it actually
became available (publication lags, revisions, month-end processing).

**Method.**
1. Record the availability date of every field used.
2. Re-run the backtest with each field lagged to when it was really known.
3. Compare performance before and after.

**Setting the pass criteria.** Any material fall in performance after
point-in-time correction is a finding; agree the materiality level first.

**What the illustration shows.** A simple rule that moves to cash after
three negative months looks brilliant when the current month's return leaks
into the signal (11.2% a year, Sharpe 1.64). Lagged by one month, it earns
3.0% a year with a Sharpe of 0.51, no better than holding the portfolio.
[`d2_look_ahead_bias.py`](../05-illustrations/d2_look_ahead_bias.py)

**Regulatory hook.** SEC IM Guidance 2017-02 (testing the algorithm);
Marketing Rule. **NIST AI RMF.** MEASURE 2.5.

---

### D3. Input drift, not just output drift

**Principle.** A datasheet asks how the data is maintained and whether the
population it describes can change. A model validated on one population is
not automatically valid on another.

**Objective.** Detect when the clients or market inputs reaching the model
move away from the population it was validated on, even if its outputs look
unchanged.

**Client harm.** The model keeps producing a familiar mix of recommendations
for a population it was never tested on.

**Why existing tests miss it.** Monitoring often watches outputs: the mix of
recommended portfolios, complaint rates. Shifts in different inputs can
cancel out in the output.

**Data.** The reference snapshot used in validation and the live population,
for each key input.

**Method.**
1. Population Stability Index (or a similar distance) per input, live against
   reference.
2. The same for the output.
3. Investigate any input that crosses its band, whatever the output does.

**Setting the pass criteria.** Agree bands per input, knowing that the usual
0.10 and 0.25 thresholds are conventions (Yurdakul, 2018). Larger samples
make small shifts look significant; small samples hide large ones.

**What the illustration shows.** After a simulated campaign brings in younger
and less experienced clients, age has a PSI of 0.52 and experience 0.70, both
well past the action band. The questionnaire score (0.005) and the
recommended mix (0.004) barely move, because younger clients score higher and
novices lower.
[`d3_input_drift_psi.py`](../05-illustrations/d3_input_drift_psi.py)

**Regulatory hook.** Duty of care, including monitoring (IA-5248).
**NIST AI RMF.** MEASURE 2.4.

---

### D4. Correlation breakdown under stress

**Principle.** The data only contains the conditions that happened during its
collection period. A portfolio built on the historical relationship between
assets depends on that relationship holding.

**Objective.** Measure how much each portfolio's risk in a crisis depends on
diversification assumptions, by stressing the relationships it relies on.

**Client harm.** The portfolio sold as safest relies most on one assumption,
and its clients are the least able to absorb the surprise if it fails.

**Why existing tests miss it.** Historical stress tests replay the past. If
bonds rallied in every crisis in the sample, the test cannot show what
happens when they do not, as in 2022.

**Data.** Asset returns over a long period; the portfolio weights.

**Method.**
1. Estimate volatilities and correlations during stress periods in the data.
2. Replace the key correlation (here equity-bond) with a plausible adverse
   value, keeping crisis volatilities.
3. Recompute each portfolio's crisis volatility and compare.

**Setting the pass criteria.** Each portfolio stays within the risk level
disclosed for stressed conditions, or the dependence on the assumption is
disclosed.

**What the illustration shows.** In the simulated crises bonds rallied
(correlation −0.32). If instead they moved with equities (+0.50), the 20/80
portfolio's crisis volatility rises by 41%, against 15% for 50/50 and 3%
for 85/15.
[`d4_stressed_correlation.py`](../05-illustrations/d4_stressed_correlation.py)

**Regulatory hook.** Duty of care (suitability). **NIST AI RMF.** MEASURE 2.6.

---

### D5. Out-of-distribution detection and abstention

**Principle.** A datasheet records what the data covers. Outside that range,
the model is extrapolating.

**Objective, method and pass criteria.** Define what counts as
in-distribution (history length and liquidity for assets; age, wealth and
answer ranges for clients) and test that cases outside it are flagged or
routed to a human at the agreed rate, using deliberately out-of-range test
cases.

**Client harm.** A client unlike anyone in the data, or a recently launched
asset with little history, receives advice with unearned confidence.

**Regulatory hook.** Duty of care. **NIST AI RMF.** MEASURE 2.5. Related: U2.

### D6. Baseline value-add

**Principle.** Elaborate allocation models often fail to beat naive ones out
of sample (DeMiguel, Garlappi & Uppal, 2009).

**Objective, method and pass criteria.** Compare the model with simple
baselines (equal weight, a static balanced mix, a market-cap rule) on the same
data and horizon. Pass if the model beats them on risk-adjusted outcomes by a
margin that survives resampling (see P2 for the interval method).

**Client harm.** Clients pay, in fees or complexity, for sophistication that
adds nothing.

**Regulatory hook.** Duty of care (best interest). **NIST AI RMF.** MEASURE 2.13.

---

### D7. Label noise and rater agreement

**Principle.** A datasheet asks who labelled the data and how. If "correct"
risk buckets were set by reviewers, the labels carry the reviewers'
disagreements.

**Objective.** Measure how consistently independent reviewers label the
same cases before those labels are used to judge the model.

**Client harm.** A model is approved or rejected on its "accuracy" against
labels that are partly noise, so real problems are missed or false ones
chased.

**Why existing tests miss it.** Labels are treated as ground truth. Their
reliability is rarely measured.

**Data.** A sample of cases labelled independently by at least two reviewers.

**Method.**
1. Raw agreement.
2. Cohen's kappa (chance-corrected), with a bootstrap interval.
3. Weighted kappa for ordered labels, and where disagreements fall.

**Setting the pass criteria.** Agree a minimum kappa per label type. Where it
falls short, use consensus labels or a second review for boundary cases
before judging the model.

**What the illustration shows.** Two simulated reviewers agree on 50% of
files. Kappa is 0.37 (interval 0.30 to 0.44); weighted kappa is 0.79,
because 93% of disagreements are one bucket apart. The labels are reliable
about direction but not about exact buckets, and that limits how precisely
any model can be judged against them.
[`d7_rater_agreement.py`](../05-illustrations/d7_rater_agreement.py)

**Regulatory hook.** SR 26-2 (model testing of data quality and relevance). **NIST AI RMF.** MEASURE 2.1.

## How the tests fit together

D1 and D2 ask whether the past shown to clients was achievable. D3 and D4 ask
whether the past still describes the present. D5 asks what happens at the
edges of the data. D6 asks whether the model earns its complexity. D7 asks
whether the yardstick itself is sound. In a validation report, I would place
D7 first: every accuracy figure depends on it.
