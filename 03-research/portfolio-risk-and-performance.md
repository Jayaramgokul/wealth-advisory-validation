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

**Data.** Daily returns for each model portfolio over a long history including
at least one stress period; the disclosed volatility or loss band.

**Method.**
1. Compute one-month 99% VaR and CVaR three ways: historical simulation (the
   actual worst months), a parametric normal model, and Monte Carlo (months
   built from randomly drawn days, which keeps fat-tailed days but loses the
   clustering of bad days).
2. Translate the disclosed band into the loss it implies at the same horizon
   and confidence.
3. Compare the worst of the three CVaRs with the band-implied loss.

**Setting the pass criteria.** Agree in advance (a) how far apart the methods
may be before the choice of method needs justifying, and (b) how far the worst
CVaR may exceed the band-implied loss before the band must be widened or the
disclosure reworded.

**What the illustration shows.** In the simulated data the normal model gives
the smallest tail loss for every portfolio. For the 85/15 portfolio,
historical CVaR is 15.2% against 11.5% from the normal model, and the
disclosed band implies about 11.4%. Monte Carlo (14.2%) sits between the two: it keeps the fat-tailed days
but not their tendency to arrive together. A band built on the normal model
looks consistent with itself and is still optimistic.
[`p1_tail_risk_three_ways.py`](../05-illustrations/p1_tail_risk_three_ways.py)

**Adjacent tests.** P5 puts intervals on the volatility figure itself; P1 asks
whether volatility is even the right summary of the tail.
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

**Data.** Daily returns per portfolio; the risk-free rate used; any claim
made in client material.

**Method.**
1. Compute Sharpe and Sortino for each portfolio.
2. Resample the history in blocks of consecutive days (moving-block
   bootstrap) many times, recomputing both ratios each time. Blocks preserve
   the clustering of volatility that single-day resampling destroys (R1).
3. For each claimed ranking, take the bootstrap distribution of the
   *difference* and its 95% interval.

**Setting the pass criteria.** A ranking is supported only if the interval of
the difference excludes zero. Agree in advance what counts as "only just"
(how close to zero the interval may come), because a fragile ranking should
not appear in marketing without qualification.

**What the illustration shows.** The individual intervals overlap heavily.
The difference between 50/50 and 85/15 excludes zero, but only just
(upper end −0.001), so the script labels the claim fragile rather than
supported.
[`p2_sharpe_sortino_intervals.py`](../05-illustrations/p2_sharpe_sortino_intervals.py)

**Adjacent tests.** R1 (dependent data) explains why ordinary bootstrap
intervals would be too narrow here; S2 (multiple testing) applies when many
pairwise rankings are claimed.
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

**Data.** Daily returns; the process that turns a volatility estimate into
exposure (here, scaling a portfolio towards its disclosed band); the band.

**Method.**
1. Forecast volatility each day with both estimators.
2. Apply the same exposure rule using each forecast.
3. Compare forecast error against realised next-month volatility, the share of
   days above 1.25 times the band, and the average exposure.

**Setting the pass criteria.** Fix materiality before running: here, a
difference of more than 2 percentage points in days in breach, or more than
0.10 in the average risk scale (the multiplier applied to exposure). Below that, record the test so the choice is
evidenced; above it, the choice needs a documented rationale.

**What the illustration shows.** EWMA forecasts slightly better (3.9% error
against 4.1%), but outcomes barely differ: breach days are within 0.1 points
and exposure differs by 0.05. Under the pre-agreed thresholds, the result is
that outcomes are robust to the choice. That is a useful finding too, as long
as it is evidenced.
[`p3_ewma_vs_sample_volatility.py`](../05-illustrations/p3_ewma_vs_sample_volatility.py)

**Adjacent tests.** D3 (input drift) would trigger a rerun when the market
regime changes; O1 (single-feature dominance) is the equivalent question for
the client-placement model.
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

**Data.** Annual returns per portfolio; the withdrawal pattern the model
assumes; the planning horizon.

**Method.**
1. Take the portfolio's annual returns over the horizon (Bengen used 30 years).
2. Reorder them many times. The average return is identical in every
   ordering; only the sequence changes.
3. Apply the withdrawal pattern each time and count how often the money runs
   out before the horizon.

**Setting the pass criteria.** Agree a maximum depletion probability for each
client segment with the business and compliance, and require that the
recommendation logic and disclosures reflect it.

**What the illustration shows.** Withdrawing 4% of the starting value each
year for 30 years, the money runs out in 0.0% of orderings for 20/80, 5.1%
for 50/50 and 24.3% for 85/15, even though 85/15 has the
highest average return and that average is the same in every ordering.

**Limitation.** Reordering one history isolates the effect of order. It does
not explore histories with different returns, so a full test would also run
the same exercise on block-bootstrapped histories (as in P5).
[`p4_sequence_of_returns.py`](../05-illustrations/p4_sequence_of_returns.py)

**Adjacent tests.** F3 reports outcomes for older clients separately; U2
routes borderline cases to a human.
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

**Data.** Daily returns per portfolio; the disclosed bands.

**Method.**
1. Block-bootstrap the return history many times.
2. Recompute annual volatility (and, if disclosed, maximum drawdown) each time.
3. Compare the 97.5th percentile with the band.

**Setting the pass criteria.** Pass if the upper end of the interval is inside
the band; otherwise widen the band or reduce the portfolio's risk. Agree the
confidence level in advance.

**What the illustration shows.** All three portfolios pass on volatility (the
85/15 upper end is 16.8% against a 17% band). Set beside P1, the same
85/15 portfolio has tail losses well beyond what that band implies.
Passing on volatility does not settle the question of tail risk, which is why
the two tests sit together.
[`p5_intervals_on_risk_metrics.py`](../05-illustrations/p5_intervals_on_risk_metrics.py)

**Adjacent tests.** P1 (tail shape); R1 (dependent data).
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
