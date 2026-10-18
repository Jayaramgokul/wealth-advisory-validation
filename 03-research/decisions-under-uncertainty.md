# Placing clients under uncertainty

> Public sources only; full references in [SOURCES.md](../SOURCES.md). Every
> number quoted below comes from the simulated data in
> [05-illustrations](../05-illustrations/), not from any real firm.

## Why this lens

Placing a client in a risk bucket is a decision made under uncertainty. The
questionnaire is a noisy measurement of risk tolerance, and the model turns
it into one of a few portfolios. Validations usually report how often the
placement is right. Decision theory asks two better questions: **what does
each kind of mistake cost the client**, and **when should the model not
decide at all?**

Bishop's *Pattern Recognition and Machine Learning* (chapter 1.5) sets this
out plainly. The best decision minimises expected loss under an explicit loss
matrix, not the error rate. When no option has a low enough expected loss,
the best decision is to refer the case (the "reject option"). And
probabilities are only useful for these decisions if they are honest.

## What I read, and what each source changed

| Source | The idea I took from it | What it changed in the tests |
|---|---|---|
| Bishop (2006), section 1.5.2, minimising expected loss | Decisions should minimise expected loss under a loss matrix, which need not be symmetric. | Expected cost becomes the headline metric (U1) |
| Bishop (2006), section 1.5.3, the reject option | Refusing to decide when uncertainty is high can lower total loss. | A refer-to-human rule set from the cost matrix (U2) |
| Bishop (2006), section 3.3, the predictive distribution | A prediction should carry its uncertainty. | Intervals on individual recommendations (U4) |
| Bishop (2006), section 3.4, Bayesian model comparison | Choosing one model discards the uncertainty about which model is right. | Testing the cost of committing to one model (U5) |
| Bishop (2006), sections 6.4 and 7.2, automatic relevance determination | Priors can switch off inputs the data does not support. | Data-supported feature use (U6) |
| Bishop (2006), chapter 13, hidden Markov models | A client's state can change over time and be inferred from behaviour. | Detecting a change in the client (U7) |
| Gneiting & Raftery (2007); Brier (1950) | Proper scoring rules reward honest probabilities; accuracy does not. | Proper scoring for every probabilistic layer (U8) |

## The tests

---

### U1. Asymmetric cost of mistakes

**Principle.** The optimal decision minimises expected loss under the loss
matrix that reflects real consequences (Bishop, 1.5.2).

**Objective.** Judge the placement model by the expected harm of its
mistakes, using a cost matrix agreed before testing, not by accuracy.

**Client harm.** A cautious client placed in an aggressive portfolio can
suffer losses they cannot bear and sell at the bottom. A client placed too
cautiously loses some return. Treating these as equal hides the worse harm.

**Why existing tests miss it.** Accuracy and confusion-matrix summaries count
mistakes without weighing them.

**Data.**
- **The band each client was placed in, and the band that was actually
  suitable,** for a test population. The suitable band comes from an agreed
  reference: an adviser's file review (with its reliability checked under
  D7), or synthetic personas whose profiles are known by construction.
- **The cost matrix:** one number for every combination of placed and
  suitable band, saying how bad that mistake is for the client. It is the
  most important input in this test, and it is a business decision, not a
  statistical one.

**Method.**
1. **Agree the cost matrix** with the business and compliance, and date it
   before any results are seen. The illustration uses a simple one: each band
   too cautious costs 1, and each band too aggressive costs 3, so placing a
   client two bands too high costs 6. A real matrix might also weigh the
   client's capacity for loss or time horizon.
2. **Compute the expected cost per client** for each candidate model: the
   average, over the test population, of the cost of each placement.
3. **Report it beside accuracy,** and beside the split of errors into too
   aggressive and too cautious, so readers can see why the ranking differs.
4. **Test sensitivity to the matrix.** Rerun with plausible alternatives,
   such as a 2:1 or 5:1 ratio. If the preferred model changes, the choice
   depends on the matrix, and that dependence should be stated.

**Setting the pass criteria.** Expected cost below an agreed limit, and no
worse than the current model or a simple benchmark. The cost matrix itself is
approved and dated before testing, because changing it after seeing results
could make any model pass.

**What the illustration shows.** The script simulates 6,000 clients with a
known suitable band, and two placement models with the same amount of noise.
Model A leans towards placing clients too high; model B leans too low.

| Model | Accuracy | Too aggressive | Too cautious | Expected cost per client |
|---|---|---|---|---|
| A | 65% | 26% | 10% | 0.88 |
| B | 62% | 10% | 29% | **0.58** |

On accuracy, model A wins by three points and would be chosen. Under the cost
matrix, its errors fall on the expensive side: a quarter of clients are
placed in too much risk. Model B makes more mistakes, but cheaper ones, and
its expected cost is a third lower. The less accurate model is the better one
for clients.
[`u1_cost_of_mistakes.py`](../05-illustrations/u1_cost_of_mistakes.py)

**Adjacent tests.**
- **G2** asks which way the errors lean for each client group.
- **U2** uses the same cost matrix to decide when to refer a client to a
  human.
- **O2** compares the model with challengers; expected cost is the right
  yardstick for that comparison.

**Regulatory hook.** Duty of care (suitability). **NIST AI RMF.** MEASURE 2.6.

---

### U2. Refer to a human when unsure

**Principle.** When the lowest expected loss of any decision is still high,
referring the case can be better than deciding (Bishop, 1.5.3).

**Objective.** Check that a refer-to-human rule exists, is set from the cost
matrix and the model's own uncertainty, and routes the right clients.

**Client harm.** The model always answers, so the clients it understands
least receive confident advice.

**Why existing tests miss it.** Model-driven advice is often judged on how many
clients it serves without intervention. Referral can be seen as failure
rather than as a control.

**Data.**
- **For each client, the model's probability of each band being the right
  one.** If the model only outputs a single band, these probabilities have to
  be estimated, for example from a separate calibration sample with known
  outcomes, as the illustration does.
- **The cost matrix** from U1.
- **The cost of a human review,** in the same units: the adviser's time, plus
  any delay to the client. This is again a business decision.

**Method.**
1. **Expected cost of every option.** For each client, multiply the band
   probabilities by the cost matrix to get the expected cost of placing them
   in each band.
2. **The rule.** Place the client in the band with the lowest expected cost,
   unless even that cost exceeds the cost of a review; then refer.
3. **Sweep the review cost.** Report total expected cost and the share of
   clients referred for a range of review costs, overall and by group. This
   gives the business a trade-off curve rather than a single answer.
4. **Check the route.** Sample referred clients and confirm that they
   actually reached a human, and that the human had what they needed to
   decide.

**Setting the pass criteria.** A referral rule exists, its threshold is
justified by the trade-off curve and the firm's review capacity, and referred
clients actually reach a human. Because U8 shows that overconfident
probabilities send too few clients for review, the rule should only be
accepted if the probabilities feeding it pass U8.

**What the illustration shows.** The script estimates each client's band
probabilities from a separate calibration sample of 40,000 simulated clients,
by questionnaire score and investment experience, and then applies the rule
to 6,000 new clients. Placing everyone costs 0.53 per client.

| Cost of a review | Expected cost per client | Referred | Novices referred | Experienced referred |
|---|---|---|---|---|
| 0.4 | 0.35 | 70% | 100% | 50% |
| 0.6 | 0.48 | 57% | 98% | 30% |
| 0.8 | 0.52 | 8% | 20% | 0% |

Referral lowers expected cost at every review cost tested, and by most when
reviews are cheap. In every row, novices are referred far more often than
experienced clients. The questionnaire measures novices less reliably (F5),
so the model is less sure about them, and the rule sends them to a human.
The weakness in measurement shows up as a workload that can be planned for.
[`u2_refer_when_unsure.py`](../05-illustrations/u2_refer_when_unsure.py)

**Adjacent tests.**
- **F5** explains why novices dominate the referrals.
- **U8** checks that the probabilities driving the rule are honest.
- **G3** sweeps thresholds by group; the review cost here is a threshold of
  the same kind.

**Regulatory hook.** Duty of care; FINRA Rule 2165 (vulnerable clients).
**NIST AI RMF.** MANAGE 2.4.

---

### U3. Dependence on protected attributes

**Principle.** Information-theoretic measures such as mutual information
detect dependence that a comparison of averages can miss.

**Objective.** Find any dependence between the model's outputs and protected
or proxy attributes, including dependence in spread or shape that averages
cannot show.

**Client harm.** Outputs depend on a protected attribute in a way that
averages do not reveal, for example through spread rather than level.

**Why existing tests miss it.** Fairness checks usually compare average
outcomes between groups. Two groups can have the same average equity share
while one is placed far more erratically than the other.

**Data.** Every output the model produces (score, band, equity share,
referral decision) for each client, with protected attributes or the
reviewed proxies from G6.

**Method.**
1. **Estimate the mutual information** between each output and each
   attribute. Mutual information is zero only if knowing the attribute tells
   you nothing at all about the output, in level, spread or shape.
2. **Get a p-value by permutation:** shuffle the attribute across clients
   many times, re-estimate each time, and see how often the shuffled value
   is as large as the real one. This avoids relying on approximations that
   break down with small groups.
3. **Control the false discovery rate** across all output-attribute pairs
   (S2).
4. **Describe any dependence found:** whether it is a shift in level (which
   F2 and F4 already cover), a difference in spread, or a difference in the
   tails.

**Setting the pass criteria.** Pass if no dependence is significant after
correction, or each significant one is explained, for example by a
legitimate suitability factor confirmed in F4.

**Adjacent tests.**
- **F2 and F4** test differences in level; U3 catches the rest.
- **S2** controls false alarms across the many pairs tested.

**Regulatory hook.** Fair treatment. **NIST AI RMF.** MEASURE 2.11.

### U4. Intervals on individual recommendations

**Principle.** A prediction should carry its uncertainty (Bishop, 3.3).

**Objective.** Give each recommendation an interval, check that the
intervals mean what they say, and make sure they are used.

**Client harm.** "Allocate 28% to equities" is presented as exact when the
model could as easily say 20% or 36%.

**Why existing tests miss it.** Recommendations are produced and tested as
single numbers, so how uncertain each one is never appears.

**Data.**
- **The model's recommendation** for each client, such as the equity share.
- **A reference for what was actually suitable,** on held-out clients, from
  the same source as U1.
- **The model's own uncertainty,** if it produces one; otherwise a held-out
  calibration sample to build intervals from.

**Method.**
1. **Produce an interval for each recommendation.** A model with a
   probabilistic form gives one directly. For any other model, split
   conformal prediction builds intervals from the errors on a calibration
   sample, with a coverage guarantee that does not depend on the model's
   internals.
2. **Check coverage on held-out clients:** do 90% intervals contain the
   suitable value about 90% of the time? Check overall and for each client
   group, since an interval can be right on average and wrong for one group.
3. **Check width.** An interval that always covers but is uselessly wide
   tells the client nothing.
4. **Check use.** Wide intervals should lead somewhere: a referral (U2), or a
   recommendation shown as a range.

**Setting the pass criteria.** Coverage within an agreed band of its stated
level (for example, 87–93% for 90% intervals) overall and in every group,
widths agreed as useful, and a documented use of the intervals downstream.

**Adjacent tests.**
- **U2** is the natural use for a wide interval.
- **U8** checks the probabilities that intervals are often built from.

**Regulatory hook.** Disclosure. **NIST AI RMF.** MEASURE 2.9.

### U5. Cost of committing to one model

**Principle.** Model comparison weighs the evidence for alternatives;
selecting one discards the uncertainty between them (Bishop, 3.4).

**Objective.** Find out whether close alternative models would have placed
clients differently, and make sure the choice between them is justified
where it matters.

**Client harm.** A client's portfolio depends on which of two equally
supported models happened to be chosen.

**Why existing tests miss it.** Validation usually tests the chosen model
alone. The other candidates from development are rarely kept, let alone
compared client by client.

**Data.** The candidate models considered during development, from the
development documentation, with their measures of fit and the ability to run
them on the same clients.

**Method.**
1. **Compare the evidence** for the close candidates: cross-validated
   expected cost from U1, or a Bayesian measure of fit where the models
   allow it.
2. **Run all close candidates on the same clients** and measure where they
   disagree: the share of clients placed in a different band, and by how
   many bands.
3. **Look at who sits in the disagreements.** If they cluster in one group,
   the choice of model is effectively a choice about that group.
4. **Choose a response:** justify the chosen model, combine the candidates,
   or refer the clients they disagree on (U2).

**Setting the pass criteria.** Agree in advance what counts as "close"
evidence and a "material" disagreement (for example, more than 5% of clients
placed in a different band). Pass if every close-and-material case has a
documented justification or response.

**Adjacent tests.**
- **O2** keeps a challenger model running against the chosen one over time.
- **U2** offers a way to handle clients the models disagree on.

**Regulatory hook.** SR 26-2 (conceptual soundness). **NIST AI RMF.** MEASURE 2.13.

### U6. Data-supported feature use

**Principle.** Automatic relevance determination lets the data switch off
inputs it does not support (Bishop, 6.4 and 7.2).

**Objective.** Identify inputs that the data does not support, and make sure
each is removed or justified.

**Client harm.** Advice depends on inputs that carry no real information,
adding noise to every placement.

**Why existing tests miss it.** Inputs are usually chosen during development
and kept by habit. Their contribution is rarely retested once the model is
in use.

**Data.** The model's training data: every input and the outcome it is
trained to predict.

**Method.**
1. **Refit with automatic relevance determination:** a prior on each input's
   weight whose strength is learned from the data. Inputs the data does not
   support have their weights shrunk towards zero.
2. **Cross-check with a simpler method:** the drop in held-out performance
   when each input is randomly shuffled. An input that ARD switches off and
   whose shuffling changes nothing is very likely unnecessary.
3. **Check stability:** does the same set of inputs come out as unsupported
   on resampled data (S3)?

**Setting the pass criteria.** Pass if each unsupported input is either
removed or kept for a documented reason, such as a regulatory requirement to
ask the question even when the answer adds little to the score.

**Adjacent tests.**
- **S3** checks that the list of important inputs is stable under
  resampling.
- **O1** checks the opposite problem: one input dominating.

**Regulatory hook.** SR 26-2. **NIST AI RMF.** MEASURE 2.9.

### U7. Detecting a change in the client

**Principle.** A hidden Markov model infers a changing hidden state from
observed behaviour (Bishop, chapter 13).

**Objective.** Test whether the firm can detect that a client's situation
has changed, so that their profile and advice are updated.

**Client harm.** A client's circumstances change but their profile stays
fixed at onboarding, so advice drifts out of suitability.

**Why existing tests miss it.** Profiles are validated at onboarding. Change
is usually caught only by a periodic review or by the client volunteering
it, which may come too late.

**Data.**
- **Client behaviour over time:** contributions and withdrawals, changes to
  regular payments, trading after market falls, updates to personal
  details.
- **Labelled examples of known changes,** such as retirement dates or events
  recorded by advisers, to test detection against.

**Method.**
1. **Define a small set of client states,** for example accumulating,
   approaching retirement, drawing an income, in financial distress.
2. **Fit a model in which clients move between these hidden states,** with
   each state producing a typical pattern of behaviour. A hidden Markov
   model is the standard form.
3. **Alert when the probability of a new state crosses a threshold.**
4. **Test on the labelled examples:** the share of real changes detected,
   how soon after the change, and how many false alarms per client per year.

**Setting the pass criteria.** Agree the detection rate, the acceptable
delay and the false-alarm rate in advance. Pass if they are met, and every
alert leads to an action, such as re-profiling or an adviser contact.

**Adjacent tests.**
- **D3** watches for change across the whole client base; U7 watches each
  client.
- **U2** gives a natural route for alerts: refer the client to a human.

**Regulatory hook.** Duty of care (monitoring). **NIST AI RMF.** MEASURE 2.4.

---

### U8. Proper scoring rules

**Principle.** A scoring rule is proper if it is optimised by reporting the
true probability (Gneiting & Raftery, 2007). Log loss and the Brier score are
proper; accuracy is not.

**Objective.** Check that every layer whose probabilities drive decisions is
trained and evaluated with a proper scoring rule.

**Client harm.** An overconfident model sends too few clients for review
(U2) and states certainties it does not have.

**Why existing tests miss it.** Accuracy and ranking measures (such as AUC)
are unchanged if probabilities are pushed towards 0 and 1, so they cannot
see overconfidence.

**Data.**
- **Every place in the model where a probability drives a decision,** such
  as the band probabilities in U2, or a prediction of whether a client will
  sell in a downturn.
- **For each,** the predicted probabilities and the actual outcomes on
  held-out data.
- **The loss function used in training,** from the development
  documentation.

**Method.**
1. **Score the probabilities** with log loss and the Brier score. Both
   reward honest probabilities: a model cannot improve its score by
   exaggerating its confidence.
2. **Check reliability:** group cases by their predicted probability and
   compare with how often the event actually happened. Among cases given
   more than 90%, the event should happen more than 90% of the time.
3. **Check the training objective.** A model trained on accuracy alone can
   be overconfident even if it is evaluated properly afterwards.

**Setting the pass criteria.** Proper scoring rules are used in training and
evaluation, and the reliability check shows no material gap at the
probabilities that drive decisions. Recalibration after training is a
clean-up step, not a substitute.

**What the illustration shows.** The script simulates 20,000 clients and the
probability that each will sell in a downturn. The overconfident model ranks
clients in exactly the same order as the calibrated one, but pushes every
probability towards 0 or 1.

| Model | Accuracy | Brier score | Log loss | Says "over 90%" for | Right in those cases |
|---|---|---|---|---|---|
| Calibrated | 71.3% | 0.188 | 0.555 | 1% of clients | 90% |
| Overconfident | 71.3% | 0.216 | 0.758 | 15% of clients | 79% |

Accuracy cannot tell the two apart, because both put every client on the
same side of 50%. The proper scores can. The overconfident model claims
near-certainty for 15% of clients and is wrong for about one in five of them.
Fed into a referral rule like U2, it would wave through clients who should
have been reviewed.
[`u8_proper_scoring.py`](../05-illustrations/u8_proper_scoring.py)

**Adjacent tests.**
- **U2** depends on honest probabilities to refer the right clients.
- **U4** builds intervals that are only as good as the probabilities beneath
  them.

**Regulatory hook.** SR 26-2. **NIST AI RMF.** MEASURE 2.5.

## How the tests fit together

U1 sets the yardstick (expected harm). U8 ensures the probabilities behind
decisions are honest. U2 uses both to decide when not to decide. U4 to U7
widen the same idea to individual recommendations, model choice, inputs and
changes over time.
