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

Tests D1 to D4 and D7 have an illustration. D5 and D6 are described in the
same structure, without one.

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

**Data.**
- **The fund or asset universe as it stood at each date,** including every
  product that later closed, merged or was delisted. Commercial databases
  sell "survivorship-free" versions for this reason; a firm's own product
  list usually is not one.
- **Returns for closed products up to their closure date,** and what happened
  to investors' money at closure (merged into another fund, or returned as
  cash).
- **Every backtest used in product design or shown to clients,** with the
  universe and dates it was built on.

**Method.**
1. **Rebuild the universe point in time:** at each date, the set of products
   an investor could actually have bought.
2. **Re-run the backtest on that universe,** holding each closed product
   until its closure date and then following the investor's money.
3. **Compare with the published result,** per year and cumulatively over the
   period shown to clients, since a small annual bias compounds.
4. **Check the selection rule,** if the backtest picks products by any
   criterion, such as "top-rated funds". The rule must use the ratings
   available at the time, not today's (D2).

**Setting the pass criteria.** Agree in advance how large a difference is
material for client communications, for example a fraction of a percent a
year. Below that, record the result. Above it, the published backtest is
withdrawn or restated. The universe definition must be documented either
way.

**What the illustration shows.** The script simulates 400 funds over ten
years. Most have a small negative return relative to the market after fees,
and a fund closes once it trails the market by 15% since launch.

| Backtest built on | Annual return |
|---|---|
| Today's survivors only | 8.92% |
| The full universe, each fund held until it closed | 7.59% |
| Bias | **+1.33% a year, +13.1% over ten years** |

181 of the 400 funds close along the way, nearly half. A backtest on the 219
survivors looks 1.3 points a year better than anything an investor could
have achieved, and over ten years the gap compounds to 13%. Elton, Gruber
and Blake found close to 1% a year in real US fund data, so the simulation
is in the same range.
[`d1_survivorship_bias.py`](../05-illustrations/d1_survivorship_bias.py)

**Adjacent tests.**
- **D2** checks the other way a backtest can use information it should not
  have: from the future.
- **D6** compares the model with simple baselines on the same honest data.
- **P2** puts intervals on the risk-adjusted returns a backtest produces.

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

**Data.** For every field the model or backtest uses:
- the date it refers to, such as the end of a month or quarter;
- the date it actually became available: publication lags, later revisions
  (economic data and company accounts are often revised), and the firm's own
  processing delays, such as month-end data that arrives a few days later.

**Method.**
1. **Record the availability date of every field,** in a table the model
   owner confirms.
2. **Re-run the backtest with each field lagged** to when it was really
   known, using the first published value rather than the revised one.
3. **Compare performance before and after,** and find which fields account
   for the difference.
4. **Check labels too.** If a model is trained to predict an outcome, any
   input recorded after the outcome, or because of it, leaks the answer.

**Setting the pass criteria.** Agree the materiality level first. Any
material fall in performance after point-in-time correction is a finding,
and the corrected figures replace the published ones.

**What the illustration shows.** The script tests a simple rule on the 50/50
portfolio over 20 simulated years: hold the portfolio while equities' last
three months add up to a gain, and move to cash otherwise.

| Version | Annual return | Sharpe ratio |
|---|---|---|
| Buy and hold | 3.91% | 0.45 |
| Rule, with this month's return leaking into the signal | 11.23% | 1.64 |
| Rule, using returns up to last month only | 2.98% | 0.51 |

With one month of look-ahead, the rule appears to almost triple the return
and more than triple the Sharpe ratio. Lagged to what was actually known, it earns less than
simply holding the portfolio, with only a slightly better Sharpe ratio. The
only difference between the two versions is a one-month shift in the data,
which is easy to miss in code.
[`d2_look_ahead_bias.py`](../05-illustrations/d2_look_ahead_bias.py)

**Adjacent tests.**
- **D1** checks the universe the backtest draws from.
- **S1** guards against the same problem in model development: choices made
  on the full data leaking into a performance estimate.

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

**Data.**
- **The reference snapshot:** the input data the model was validated on,
  kept unchanged.
- **The live population,** for each monitoring period, with the same fields.
- **The list of key inputs to watch,** agreed with the model owner: the
  client characteristics and market inputs the model depends on most (O1
  helps find them).

**Method.**
1. **Compute the Population Stability Index** (or a similar distance) for
   each input, live against reference. PSI compares the share of clients in
   each range of the input; zero means no change.
2. **Do the same for the outputs,** such as the recommended band.
3. **Investigate any input that crosses its band,** whatever the output does.
   An input shift with a stable output is the most important case, because
   output monitoring alone would never raise it.
4. **Find the reason** for each shift: a marketing campaign, a new channel, a
   change in how data is recorded, or a change in the market.

**Setting the pass criteria.** Agree bands per input, knowing that the usual
0.10 ("watch") and 0.25 ("act") thresholds are conventions, not tests with
known error rates (Yurdakul, 2018). With large samples, small and harmless
shifts can cross them; with small samples, large shifts may not. Pass if
every input is within its band, or every crossing has been investigated and
either explained or acted on, for example by revalidating the model on the
new population.

**What the illustration shows.** The script compares 4,000 reference clients
with 4,000 new clients brought in by a simulated campaign that attracts
younger, less experienced investors: an average age of 36 instead of 45, and
80% novices instead of 40%.

| Measure | PSI | Band |
|---|---|---|
| Age (input) | 0.52 | act |
| Share of experienced investors (input) | 0.70 | act |
| Questionnaire score | 0.005 | stable |
| Recommended band (output) | 0.004 | stable |

Both inputs are far past the action band, yet the score and the
recommendation mix barely move: 22% of new clients go to the highest band
against 21% before. Younger clients tend to score higher and novices lower,
so the two shifts cancel out in the output. Output monitoring would see
nothing, while the model is now serving a population it was never validated
on, and one it measures less reliably (F5).
[`d3_input_drift_psi.py`](../05-illustrations/d3_input_drift_psi.py)

**Adjacent tests.**
- **R2** asks in advance which changes in the world would break the model;
  D3 watches for them.
- **F9** repeats fairness testing on production data, which drift makes
  necessary.
- **U7** watches for change in individual clients rather than the whole
  population.

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

**Data.**
- **Asset returns over a long period,** with crisis periods identified.
- **The portfolio weights** for each model portfolio.
- **The risk level disclosed for stressed conditions,** if the firm
  discloses one, or the general risk band otherwise.

**Method.**
1. **Estimate volatilities and correlations during stress periods** in the
   data, separately from calm periods.
2. **Replace the key correlation with a plausible adverse value,** keeping
   crisis volatilities. For balanced portfolios the key one is usually
   between equities and bonds; +0.5 roughly matches 2022, when both fell
   together.
3. **Recompute each portfolio's crisis volatility** with the stressed
   correlation, and compare with the volatility in the data.
4. **Repeat for other relationships** the portfolios rely on, such as
   between regions or between bonds of different credit quality.

**Setting the pass criteria.** Pass if each portfolio stays within the risk
level disclosed for stressed conditions under the adverse correlation.
Otherwise, the dependence on the assumption is disclosed to clients, or the
portfolio is changed.

**What the illustration shows.** In the simulated data, equities and bonds
are mildly positively correlated in calm periods (+0.13), and bonds rally
during crises (−0.32). The test asks what happens if, in the next crisis,
they move together instead (+0.50).

| Portfolio | Crisis volatility, as in the data | If the hedge fails | Increase |
|---|---|---|---|
| 20/80 | 7.5% | 10.6% | **+41%** |
| 50/50 | 18.3% | 21.0% | +15% |
| 85/15 | 32.2% | 33.0% | +3% |

The most cautious portfolio is the most exposed to the assumption, because
its safety comes from the bonds. Its crisis volatility rises by 41%, against
3% for the most aggressive portfolio, whose clients already expect large
swings. The clients least able to absorb a surprise are the ones the
historical data reassures most.
[`d4_stressed_correlation.py`](../05-illustrations/d4_stressed_correlation.py)

**Adjacent tests.**
- **P1** measures tail losses from the history; D4 asks what the history
  does not contain.
- **P5** puts intervals on the disclosed volatility; the stressed figure is a
  different and harder test.
- **R2** lists the assumptions, like this one, whose failure would break the
  model.

**Regulatory hook.** Duty of care (suitability). **NIST AI RMF.** MEASURE 2.6.

---

### D5. Out-of-distribution detection and abstention

**Principle.** A datasheet records what the data covers. Outside that range,
the model is extrapolating.

**Objective.** Make sure the model recognises cases unlike anything in its
data, and flags them or refers them to a human rather than advising with
unearned confidence.

**Client harm.** A client unlike anyone in the data, or a recently launched
asset with little history, receives advice with unearned confidence.

**Why existing tests miss it.** Tests are drawn from the same data the model
was built on, so they rarely contain cases outside its range.

**Data.** The ranges the training data covers for each input, and a set of
deliberately out-of-range test cases built by the validator.

**Method.**
1. **Define what counts as in-distribution,** with the model owner: for
   assets, the minimum history length and liquidity; for clients, the ranges
   of age, wealth and questionnaire answers seen in the data, and unusual
   combinations of them.
2. **Build test cases outside those ranges:** a client of 85, an extremely
   wealthy client, contradictory answers, a fund launched last year.
3. **Run them through the model** and check what happens to each: flagged,
   referred, or advised as normal.
4. **Check live data** for how often such cases occur, so the referral
   workload is known.

**Setting the pass criteria.** Agree the rate at which out-of-range cases
must be flagged or referred (normally all of them). Pass if the test cases
are caught at that rate, and live cases reach a human.

**Adjacent tests.**
- **U2** provides the referral route.
- **G5** checks whether the validation data covers the client base.

**Regulatory hook.** Duty of care. **NIST AI RMF.** MEASURE 2.5.

### D6. Baseline value-add

**Principle.** Elaborate allocation models often fail to beat naive ones out
of sample (DeMiguel, Garlappi & Uppal, 2009).

**Objective.** Show that the model earns its complexity by beating simple
alternatives on the outcomes that matter to clients.

**Client harm.** Clients pay, in fees or complexity, for sophistication that
adds nothing.

**Why existing tests miss it.** Models are usually tested against their own
targets or their previous version, not against a deliberately simple rule.

**Data.** The model's recommendations and outcomes over a test period, the
same data for the baselines, and the fees or costs that the model's
complexity adds.

**Method.**
1. **Choose simple baselines** that a sensible adviser might use: equal
   weights across the asset classes, a static balanced mix for each risk
   band, or market-capitalisation weights.
2. **Run them on the same data and horizon** as the model, out of sample.
3. **Compare risk-adjusted outcomes after costs,** with intervals from a
   block bootstrap, as in P2.
4. **Look at where the model wins,** in which market conditions and for
   which clients, and whether those gains are worth the added cost.

**Setting the pass criteria.** Pass if the model beats the baselines, after
costs, by a margin that survives resampling. If it does not, the complexity
needs a reason other than performance, such as better tailoring to client
circumstances, and that reason should be tested in turn.

**Adjacent tests.**
- **P2** provides the interval method.
- **O2** keeps a challenger running against the model over time; a simple
  baseline is a good permanent challenger.

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

**Data.**
- **A sample of client files labelled independently by at least two
  reviewers,** who do not see each other's labels or the model's output.
- **The labelling guidance** the reviewers worked from, since vague guidance
  is a common cause of disagreement.
- **Enough cases near each band boundary,** where disagreement is most
  likely and matters most.

**Method.**
1. **Raw agreement:** the share of files on which the reviewers chose the
   same band.
2. **Cohen's kappa,** which corrects for the agreement expected by chance,
   with a bootstrap interval. Kappa of 1 is perfect agreement; 0 is no better
   than chance.
3. **Weighted kappa,** which counts a near miss (one band apart) as a smaller
   disagreement than a far one. Bands are ordered, so this is the fairer
   measure of how far apart the reviewers really are.
4. **Look at where disagreements fall,** by band and by type of client, to
   find what the guidance leaves unclear.

**Setting the pass criteria.** Agree a minimum kappa for each type of label
before the labels are used. Where it falls short, use consensus labels or a
second review for boundary cases before judging the model. Report the
model's accuracy against the labels alongside the reviewers' agreement with
each other: a model cannot be judged more precisely than its labels allow.

**What the illustration shows.** The script simulates two reviewers labelling
the same 300 client files into five bands. Each sees the client's true
profile with some error of their own.

| Measure | Value |
|---|---|
| Raw agreement | 50% |
| Cohen's kappa | 0.37 (95% interval 0.30 to 0.44) |
| Weighted kappa | 0.79 |
| Disagreements that are one band apart | 93% |

The reviewers disagree on half the files, and kappa says their agreement on
exact bands is only fair. But almost all their disagreements are near misses,
so weighted kappa is high. The labels are reliable about direction, but not
about exact bands. A model scored as "50% accurate" against one reviewer's
labels might be no worse than the second reviewer.
[`d7_rater_agreement.py`](../05-illustrations/d7_rater_agreement.py)

**Adjacent tests.**
- **U1** and **G2** depend on these labels to say whether a placement was
  too aggressive or too cautious.
- **F5** applies the same idea, reliability of measurement, to the
  questionnaire.

**Regulatory hook.** SR 26-2 (model testing of data quality and relevance). **NIST AI RMF.** MEASURE 2.1.

## How the tests fit together

D1 and D2 ask whether the past shown to clients was achievable. D3 and D4 ask
whether the past still describes the present. D5 asks what happens at the
edges of the data. D6 asks whether the model earns its complexity. D7 asks
whether the yardstick itself is sound. In a validation report, I would place
D7 first: every accuracy figure depends on it.
