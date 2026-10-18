# Portfolio risk and performance

> Public sources only; full references in [SOURCES.md](../SOURCES.md). Every
> number quoted below comes from the simulated data in
> [05-illustrations](../05-illustrations/), not from any real firm.

## Why this lens

A wealth manager tells every client two things about their portfolio: how
much it might lose, and how well it has done for the risk taken. Those numbers
appear in onboarding screens, factsheets and marketing, so they sit under the
duty of care, the disclosure expectations in the SEC's 2017 guidance,
and the Marketing Rule's requirement that performance be fair and balanced and
that claims be capable of substantiation.

A standard model review checks that these numbers are *calculated* correctly.
The question this lens asks is different: **do they still hold when measured
another reasonable way?** A risk figure that changes materially with the
choice of method, window or sample is not something a client should rely on.

## What I read, and what each source changed

| Source | The idea I took from it | What it changed in the tests |
|---|---|---|
| Artzner et al. (1999), *Coherent Measures of Risk* | A sensible risk measure should satisfy a few properties, including that diversifying should never look riskier. VaR can fail this; it also says nothing about how bad losses are beyond it. | Report CVaR beside VaR, never VaR alone (P1) |
| Rockafellar & Uryasev (2000); Acerbi & Tasche (2002) | CVaR, the average loss beyond VaR, is coherent and practical to estimate. | CVaR becomes the tail figure compared with the disclosed band (P1) |
| Sharpe (1966, 1994); Sortino & Price (1994) | Return per unit of risk; Sortino counts only downside volatility, which matches how clients experience risk. | Both ratios, side by side (P2) |
| Lo (2002), *The Statistics of Sharpe Ratios* | A Sharpe ratio is an estimate with a standard error, and dependence in returns distorts it. | Every ranking claim needs an interval (P2) |
| J.P. Morgan/Reuters (1996), *RiskMetrics* | Exponentially weighted volatility (λ = 0.94 for daily data) reacts to new information; an equal-weighted window remembers calm periods. | Test whether the estimator choice changes client outcomes (P3) |
| Bengen (1994), *Determining Withdrawal Rates Using Historical Data* | For someone drawing an income, the *order* of returns matters, not just the average. | A separate test for decumulating clients (P4) |
| Efron (1979); Künsch (1989) | The bootstrap gives intervals without assuming a distribution; resampling *blocks* of days keeps the clustering of volatility. | Intervals on every disclosed risk metric (P2, P5) |

## The simulated market used in the illustrations

All five illustrations use the same 20 years of simulated daily returns for
three assets: equities, high-quality bonds and cash. The market switches
between calm spells and crisis spells. A crisis starts on about 1 day in 250
and, once started, usually lasts several weeks. In a crisis, equities fall
and become far more volatile while bonds rally, and every day carries a
fat-tailed shock that hits all assets at once. The three model portfolios
are named by their equity share: **20/80**, **50/50** and **85/15**. Their
disclosed annual volatility bands are 6%, 11% and 17%.

Because the data is simulated, the "truth" is known: the tails really are
fatter than a normal distribution, and bad days really do cluster. A real
validation would use the firm's own return history in the same way.

## The tests

Each test below has the same structure. Pass criteria are written as
*how to set them*, because the bar is agreed with the model owner before the
test is run, not chosen afterwards.

---

### P1. Tail risk, three ways

**Principle.** VaR answers "how bad is a bad month at the 99th percentile",
but not "how bad, on average, are the months beyond that". CVaR answers the
second question and is a coherent risk measure (Artzner et al.; Rockafellar &
Uryasev). Different estimation methods embed different assumptions about the
tails, so disagreement between them is itself information.

**Objective.** Check that the loss figure implied by a portfolio's disclosed
risk band is not optimistic compared with the tail losses the portfolio
actually shows.

**Client harm.** A client chooses a portfolio believing a bad year costs
around X%, and experiences a materially larger loss that the firm's own data
could have shown.

**Why existing tests miss it.** A typical review recalculates the disclosed
figure using the firm's chosen method. If that method is a normal
(parametric) model, the recalculation agrees with itself and the fat tails are
never examined.

**Data.**
- **Daily returns for each model portfolio** over as long a history as the
  firm has, and at least one full stress period (2008, March 2020, 2022). A
  history without a stress period cannot say anything about the tail. Where
  a portfolio is newer than that, its current weights can be applied to the
  underlying assets' longer history, provided the reconstruction is stated.
- **The disclosed risk figure,** exactly as clients see it: a volatility
  band, a "typical worst year", or a loss range. Its wording decides which
  horizon and confidence level the test should use.
- **The method behind the disclosed figure,** from the model documentation,
  so the test knows which assumption it is checking.

**Method.**
1. **Build monthly losses** from the daily returns: rolling 21-trading-day
   sums, so every month-long window in the history counts.
2. **Estimate one-month 99% VaR and CVaR three ways:**
   - **historical simulation,** the actual worst months in the history;
   - **a normal (parametric) model,** using the average and standard
     deviation of monthly returns, which is what most volatility-based
     disclosures assume implicitly;
   - **Monte Carlo,** building many months from randomly drawn days. This
     keeps the fat-tailed days but loses the tendency of bad days to arrive
     together.
3. **Translate the disclosed band into a loss** at the same horizon and
   confidence. For a volatility band, this is the 99% point of a normal
   distribution: about 2.33 times the band divided by the square root of 12.
4. **Compare,** reporting how far apart the three methods are, and the ratio
   of the worst CVaR to the band-implied loss.

**Setting the pass criteria.** Agree two numbers in advance:
- **How far apart the methods may be** before the choice of method needs a
  written justification. A normal model well below the historical figure is
  the usual sign that the disclosure understates the tail.
- **How far the worst CVaR may exceed the band-implied loss** before the band
  must be widened, or the disclosure reworded to describe tail losses
  separately.

The second threshold is a judgement about what clients would reasonably take
the band to mean. A band presented as "how much you could lose" deserves a
tighter threshold than one clearly labelled as typical volatility.

**What the illustration shows.**

| Portfolio | Historical CVaR | Normal-model CVaR | Monte Carlo CVaR | Loss implied by the band | Worst CVaR ÷ band |
|---|---|---|---|---|---|
| 20/80 | 4.1% | 3.3% | 4.6% | 4.0% | 1.1× |
| 50/50 | 8.7% | 6.8% | 8.6% | 7.4% | 1.2× |
| 85/15 | 15.2% | 11.5% | 14.2% | 11.4% | 1.3× |

The normal model gives the smallest tail loss for every portfolio, and it
agrees with the band almost exactly. A review that recalculated the
disclosure with the same normal model would pass it. The actual history says
the worst months of the 85/15 portfolio average 15.2%, a third more than the
band implies. Monte Carlo sits between the two because it keeps the
fat-tailed days but not their clustering, which is a reminder that the
clustering itself carries risk. The gap grows with the equity share, so the
clients told the most about risk are told the least accurately.
[`p1_tail_risk_three_ways.py`](../05-illustrations/p1_tail_risk_three_ways.py)

**Adjacent tests.**
- **P5** asks whether the volatility figure itself is reliable. P1 asks
  whether volatility is even the right summary of the tail; a portfolio can
  pass P5 and fail P1, as these illustrations show.
- **D4** stresses the correlations between assets, which drive how
  portfolios lose money together in a crisis.
- **R1** explains why returns must be treated as dependent when building
  intervals for any of these figures.

**Regulatory hook.** Disclosure of risks and limitations (SEC IM Guidance
2017-02); Marketing Rule fair and balanced presentation.
**NIST AI RMF.** MEASURE 2.5 (valid and reliable; limits of generalisation documented).

---

### P2. Risk-adjusted returns with intervals

**Principle.** A Sharpe or Sortino ratio is an estimate from a finite,
dependent sample. Its standard error is often as large as the differences
between portfolios that marketing material ranks (Lo, 2002).

**Objective.** Check that any statement that one portfolio delivers better
risk-adjusted returns than another survives its own uncertainty.

**Client harm.** Clients are steered to, or reassured by, a "better"
portfolio whose advantage is noise.

**Why existing tests miss it.** Reviews check that the ratio is computed with
the right formula and risk-free rate. They rarely ask whether the comparison
is statistically supported.

**Data.**
- **Daily returns for each portfolio,** over the period the claim refers to.
- **The risk-free rate** used to compute excess returns, and its source.
- **Every claim in client material** that ranks or compares portfolios on
  risk-adjusted return, word for word, with the period it covers. The claim
  decides which comparison is tested; a claim about the last three years is
  tested on those three years, not on the full history.

**Method.**
1. **Compute the ratios.** Sharpe: average excess return over its standard
   deviation, annualised. Sortino: the same, but dividing by downside
   deviation only, which counts only the days that lose money.
2. **Resample the history in blocks** of consecutive days (a moving-block
   bootstrap, 21-day blocks here), 1,000 times, recomputing the ratios each
   time. Resampling single days would treat every day as independent and
   destroy the clustering of volatility, giving intervals that are too narrow
   (R1).
3. **Test the claim, not just each ratio.** Overlapping intervals for two
   portfolios do not settle a comparison either way. For each claimed
   ranking, take the bootstrap distribution of the *difference* in ratios and
   its 95% interval.
4. **Report** each ratio with its interval, and each claimed difference with
   its interval and verdict.

**Setting the pass criteria.**
- **Supported:** the interval of the difference excludes zero with room to
  spare.
- **Fragile:** it excludes zero, but its nearer end is within an agreed
  margin of zero (here 0.02). A slightly different history could reverse it,
  so the claim should not appear in marketing without qualification.
- **Not supported:** the interval includes zero. The claim should be
  withdrawn.

The margin for "fragile" is agreed in advance with compliance, because it
decides which claims reach clients.

**What the illustration shows.**

| Portfolio | Sharpe (95% interval) | Sortino (95% interval) |
|---|---|---|
| 20/80 | 0.41 (−0.01 to 0.84) | 0.56 (0.06 to 1.31) |
| 50/50 | 0.24 (−0.19 to 0.69) | 0.33 (−0.16 to 1.06) |
| 85/15 | 0.14 (−0.29 to 0.58) | 0.19 (−0.26 to 0.86) |

Every interval is wide, and every pair overlaps heavily. Taken one at a time,
they suggest that nothing can be said. The direct comparison of 85/15 with
50/50 is sharper: the Sharpe difference is −0.093, with an interval of
−0.186 to −0.001. The interval excludes zero, so 50/50 did deliver the
better risk-adjusted return, but its upper end is within 0.001 of zero. Under
the agreed margin, the claim is fragile and would need qualifying before it
appeared in client material.
[`p2_sharpe_sortino_intervals.py`](../05-illustrations/p2_sharpe_sortino_intervals.py)

**Adjacent tests.**
- **R1** explains why ordinary bootstrap intervals would be too narrow here.
- **S2** applies when many pairwise rankings are claimed at once: with three
  portfolios there are three comparisons, and the chance of a spurious
  "winner" grows with every one.
- **C1** uses the same comparative logic for own-brand products against a
  neutral benchmark.

**Regulatory hook.** Marketing Rule: performance fair and balanced; a
reasonable basis to substantiate material statements of fact.
**NIST AI RMF.** MEASURE 2.5.

---

### P3. Volatility estimator sensitivity

**Principle.** The RiskMetrics EWMA estimator weights recent days more
heavily (λ = 0.94); a one-year equal-weighted window does not. Each is a
defensible modelling choice. SR 26-2 lists comparing alternative assumptions
and methodologies as part of model testing, and this is exactly that kind of
choice.

**Objective.** Find out whether the choice of volatility estimator changes
what the client experiences: how much risk they hold, and how often the
portfolio runs above its disclosed band.

**Client harm.** If outcomes depend on an undocumented parameter choice,
clients carry risk that nobody decided they should carry.

**Why existing tests miss it.** A review usually validates the estimator the
firm uses. It does not rerun the process with a reasonable alternative and
compare outcomes.

**Data.**
- **Daily returns** for the portfolio, over a history with both calm and
  stressed periods, since that is where the estimators differ.
- **The rule that turns a volatility forecast into exposure.** Here, the
  portfolio's exposure is scaled each day towards its disclosed band (band ÷
  forecast, capped at 1.5). In a real model it might be a rebalancing
  trigger or a risk-band assignment.
- **The disclosed band** the rule targets.
- **The estimator the firm actually uses,** with its parameters, and at least
  one reasonable alternative.

**Method.**
1. **Forecast volatility each day with both estimators,** using only data
   available that day: a one-year equal-weighted standard deviation, and an
   EWMA with λ = 0.94.
2. **Apply the same exposure rule** with each forecast.
3. **Compare three things:**
   - **forecast error:** how far each forecast is from the volatility
     actually realised over the next month;
   - **breaches:** the share of days on which the held portfolio's
     volatility runs above 1.25 times the band;
   - **average exposure:** the average scaling applied, which is how much
     risk clients actually carried.
4. **Look at the stress periods separately.** EWMA reacts within days to a
   crisis, while a one-year window takes months; an average over 20 years can
   hide a large difference during the weeks that matter most.

**Setting the pass criteria.** Fix materiality before running. Here: a
difference of more than 2 percentage points in the share of days in breach,
or more than 0.10 in the average exposure scale.
- **Below both:** outcomes are robust to the choice. Record the test, so the
  choice is evidenced.
- **Above either:** the choice is material, and needs a documented rationale
  and sign-off. Material differences concentrated in stress periods should
  be reported separately.

**What the illustration shows.** On the 50/50 portfolio, EWMA forecasts
slightly better: its average error is 3.9 percentage points against 4.1 for
the one-year window. Client outcomes barely differ. Both put the portfolio
above 1.25 times its band on 17.9% of days, and the average exposure scale is
1.25 against 1.30, a difference of 0.05. Under the pre-agreed thresholds, the
result is that outcomes are robust to the choice.

That is a useful finding too, because the firm can now say why the choice of
estimator does not matter for clients, with evidence. The high breach rate
under either estimator is a separate point: it says the exposure rule itself
lets volatility run well above the band in crises, whichever forecast feeds
it.
[`p3_ewma_vs_sample_volatility.py`](../05-illustrations/p3_ewma_vs_sample_volatility.py)

**Adjacent tests.**
- **D3** watches for changes in market conditions or inputs that would make
  the test worth rerunning.
- **O1** asks the same kind of question for the client-placement model:
  whether one input or choice drives the outcome.
- **O2** and **O3** compare the whole model with challengers; P3 is a
  focused challenger test for one component.

**Regulatory hook.** SR 26-2: conceptual soundness; testing alternative assumptions and methodologies.
**NIST AI RMF.** MEASURE 2.5.

---

### P4. Sequence-of-returns risk for retirees

**Principle.** For a client making withdrawals, losses early in retirement do
lasting damage, because units sold at low prices are never recovered. Two
clients with the same average return can have very different outcomes (Bengen,
1994).

**Objective.** Measure how often a portfolio recommended to a decumulating
client runs out of money when the same returns arrive in a different order.

**Client harm.** A retiree is placed in a portfolio whose average return looks
ample but whose ordering risk could exhaust their savings.

**Why existing tests miss it.** Suitability reviews tend to look at expected
return and volatility, the right lens for someone saving. They do not change
the lens when the client starts drawing an income.

**Data.**
- **Annual returns for each portfolio** recommended to clients in
  decumulation, over a long history.
- **The withdrawal pattern the model assumes:** a fixed amount, a fixed
  percentage of the current balance, or an amount rising with inflation.
  Bengen's 4% rule uses the last of these, and the choice changes the answer
  considerably.
- **The planning horizon** the model uses, such as 30 years, and whether it
  varies with the client's age.
- **Which clients the model treats as decumulating,** so the test is applied
  to the portfolios those clients are actually offered.

**Method.**
1. **Take the portfolio's annual returns** over the planning horizon.
2. **Reorder them many times** (5,000 here). Every ordering contains exactly
   the same returns, so the average return is identical in all of them; only
   the sequence changes.
3. **Apply the withdrawal pattern** to each ordering, year by year, and
   record whether the money runs out before the horizon, and when.
4. **Report the depletion probability** per portfolio, and the spread of
   ending wealth, from the worst orderings to the best.

**Setting the pass criteria.** Agree a maximum depletion probability for each
client segment with the business and compliance. A client with other secure
income can carry more depletion risk than one relying on the portfolio
alone. Then require that:
- the recommendation logic does not place decumulating clients in portfolios
  above that limit;
- disclosures for decumulating clients describe the sequence risk in plain
  terms.

**What the illustration shows.** The script turns 30 years of simulated
daily returns into 30 annual returns per portfolio, and withdraws 4% of the
starting value each year, a fixed amount rather than one rising with
inflation.

| Portfolio | Average annual return | Runs out within 30 years |
|---|---|---|
| 20/80 | 3.2% | 0.0% of orderings |
| 50/50 | 3.9% | 5.1% of orderings |
| 85/15 | 4.6% | 24.3% of orderings |

The 85/15 portfolio has the highest average return, and that average is the
same in every ordering, yet it runs out in nearly a quarter of them. The
chart shows the reason: the same returns with the bad years first and with
the good years first lead to opposite outcomes. A suitability check based on
average return and volatility would rank 85/15 as the better choice for
growth, and miss that it is the riskiest choice for someone drawing an
income.

**Limitation.** Reordering one history isolates the effect of order. It does
not explore histories with different returns, so a full test would also run
the same exercise on block-bootstrapped histories (as in P5).
[`p4_sequence_of_returns.py`](../05-illustrations/p4_sequence_of_returns.py)

**Adjacent tests.**
- **F3** reports outcomes for older clients separately, so a poor result for
  them is not hidden in an average.
- **U2** routes borderline cases, such as a client close to retirement with
  no other income, to a human adviser.
- **U1** weighs the cost of mistakes; for a retiree, too much risk is
  usually the costlier error.

**Regulatory hook.** Duty of care (IA-5248); retirement accounts (DOL PTE
2020-02); senior investors (FINRA Rule 2165).
**NIST AI RMF.** MEASURE 2.6 (safety risks evaluated; residual risk within tolerance).

---

### P5. Confidence intervals on risk metrics

**Principle.** A disclosed volatility or drawdown is a point estimate. Its
interval (Efron, 1979), computed with blocks to respect dependence (Künsch,
1989), shows how bad it could plausibly be.

**Objective.** Check that the *upper end* of each portfolio's risk interval,
not just the point estimate, sits inside the disclosed band.

**Client harm.** A band that holds only at the point estimate will be breached
by an ordinary bad stretch, and the client was never told that was likely.

**Why existing tests miss it.** Reviews compare the point estimate with the
band. A point estimate inside the band looks like a pass.

**Data.**
- **Daily returns per portfolio** over the history used to set the band.
- **Each disclosed figure,** with its definition: annual volatility, maximum
  drawdown, or both.
- **The period the disclosure is meant to cover,** since a band described as
  "long-run" should be tested on a long history.

**Method.**
1. **Block-bootstrap the return history** 1,000 times, drawing 21-day blocks
   of consecutive days so that volatile spells stay together.
2. **Recompute each disclosed metric** on every resampled history: annual
   volatility and, if disclosed, maximum drawdown.
3. **Take the 2.5th and 97.5th percentiles** as the 95% interval.
4. **Compare the upper end with the band,** for each portfolio and each
   metric.

**Setting the pass criteria.** Agree the confidence level in advance (95%
here).
- **Pass:** the upper end of the interval is inside the band.
- **Fail:** the upper end is outside, even if the point estimate is inside.
  The remedy is to widen the band, reduce the portfolio's risk, or state the
  uncertainty in the disclosure.

**What the illustration shows.**

| Portfolio | Annual volatility (95% interval) | Disclosed band | Verdict |
|---|---|---|---|
| 20/80 | 4.8% (4.4% to 5.2%) | 6% | Inside |
| 50/50 | 9.3% (8.4% to 10.1%) | 11% | Inside |
| 85/15 | 15.3% (13.8% to 16.8%) | 17% | Inside, with little room |

All three portfolios pass on volatility. The 85/15 upper end, 16.8% against a
17% band, leaves almost no margin. Set beside P1, the same 85/15 portfolio
has tail losses a third larger than its band implies. Passing on volatility
does not settle the question of tail risk, which is why the two tests sit
together.
[`p5_intervals_on_risk_metrics.py`](../05-illustrations/p5_intervals_on_risk_metrics.py)

**Adjacent tests.**
- **P1** tests the shape of the tail, which volatility does not describe.
- **R1** explains why the bootstrap must use blocks of days.
- **D4** shows how stressed correlations widen the range further.

**Regulatory hook.** Disclosure of risks (SEC IM Guidance 2017-02); Marketing
Rule.
**NIST AI RMF.** MEASURE 2.5.

## How the five tests fit together

P5 asks whether the disclosed band holds on average; P1 asks whether it holds
in the tail; P2 asks whether claims of superiority are real; P3 asks whether
the numbers depend on a modelling choice; P4 asks whether the right question
is being asked at all for clients drawing an income. A portfolio can pass one
and fail another, as the P1 and P5 results above show, so they are reported
together.
