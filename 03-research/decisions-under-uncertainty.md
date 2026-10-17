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

**Data.** True and placed buckets for a test population (from reviewer labels
checked under D7, or synthetic personas with known profiles).

**Method.**
1. Agree a cost matrix with the business and compliance. Here, each step too
   aggressive costs three times a step too cautious.
2. Compute expected cost per client for each candidate model.
3. Report it beside accuracy and the split of errors by direction.

**Setting the pass criteria.** Expected cost below an agreed limit. The cost
matrix itself is approved and dated before testing.

**What the illustration shows.** Model A is more accurate (65% against 62%)
but errs towards too much risk (26% of clients). Model B errs towards caution.
Under the cost matrix, A's expected cost is 0.88 per client against B's 0.58:
the less accurate model is better for clients.
[`u1_cost_of_mistakes.py`](../05-illustrations/u1_cost_of_mistakes.py)

**Adjacent tests.** G2 asks the same question by client group.
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

**Data.** For each client, the model's probabilities over buckets; the cost
matrix; the cost of a human review.

**Method.**
1. For each client, compute the expected cost of each possible placement.
2. Refer if the lowest of these exceeds the cost of a review.
3. Report total expected cost, and the share referred overall and by group,
   for a range of review costs.

**Setting the pass criteria.** A referral rule exists, its threshold is
justified by the trade-off curve, and referred clients actually reach a human.

**What the illustration shows.** At a review cost of 0.6, referring 57% of
clients cuts expected cost from 0.53 to 0.48. Almost all novices are referred
(98%) against 30% of experienced clients. At a higher review cost (0.8),
referrals fall to 8%, still mostly novices. The questionnaire's weakness for
novices (F5) shows up here as a workload.
[`u2_refer_when_unsure.py`](../05-illustrations/u2_refer_when_unsure.py)

**Adjacent tests.** F5 (measurement reliability), U8 (honest probabilities).
**Regulatory hook.** Duty of care; FINRA Rule 2165 (vulnerable clients).
**NIST AI RMF.** MANAGE 2.4.

---

### U3. Dependence on protected attributes

**Principle.** Information-theoretic measures such as mutual information
detect dependence that a comparison of averages can miss.

**Objective, method and pass criteria.** Estimate the mutual information
between each output and each protected or proxy attribute, with intervals
and multiple-testing control (S2). Pass if no dependence is significant, or
each is explained.

**Client harm.** Outputs depend on a protected attribute in a way that
averages do not reveal, for example through spread rather than level.

**Regulatory hook.** Fair treatment. **NIST AI RMF.** MEASURE 2.11. Related: F2, F4.

### U4. Intervals on individual recommendations

**Principle.** A prediction should carry its uncertainty (Bishop, 3.3).

**Objective, method and pass criteria.** Produce a predictive interval for
each recommendation (for example, the equity share), and check on held-out
data that 90% intervals contain the outcome about 90% of the time. Pass if
the intervals are calibrated and used downstream (for example, in U2).

**Client harm.** "Allocate 28% to equities" is presented as exact when the
model could as easily say 20% or 36%.

**Regulatory hook.** Disclosure. **NIST AI RMF.** MEASURE 2.9.

### U5. Cost of committing to one model

**Principle.** Model comparison weighs the evidence for alternatives;
selecting one discards the uncertainty between them (Bishop, 3.4).

**Objective, method and pass criteria.** Compare the evidence for close
candidate models and where their recommendations disagree. Pass if the
choice is justified wherever alternatives are close and disagree materially.

**Client harm.** A client's portfolio depends on which of two equally
supported models happened to be chosen.

**Regulatory hook.** SR 26-2 (conceptual soundness). **NIST AI RMF.** MEASURE 2.13. Related: O2.

### U6. Data-supported feature use

**Principle.** Automatic relevance determination lets the data switch off
inputs it does not support (Bishop, 6.4 and 7.2).

**Objective, method and pass criteria.** Refit with ARD-style priors and
list inputs the data does not support. Pass if each is removed or its use is
justified on other grounds.

**Client harm.** Advice depends on inputs that carry no real information,
adding noise to every placement.

**Regulatory hook.** SR 26-2. **NIST AI RMF.** MEASURE 2.9. Related: S3.

### U7. Detecting a change in the client

**Principle.** A hidden Markov model infers a changing hidden state from
observed behaviour (Bishop, chapter 13).

**Objective, method and pass criteria.** Model clients as moving between
hidden states (for example, accumulating, approaching retirement, in
distress), and test detection on labelled examples. Pass if changes are
detected at the agreed rate with an acceptable false-alarm rate.

**Client harm.** A client's circumstances change but their profile stays
fixed at onboarding, so advice drifts out of suitability.

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

**Data.** Predicted probabilities and outcomes on held-out data.

**Method.**
1. Log loss and Brier score per model.
2. A reliability check: among cases given a probability above 90%, how often
   does the event happen?

**Setting the pass criteria.** Proper scoring rules are used in training and
evaluation; recalibration is a clean-up step, not a substitute.

**What the illustration shows.** Two models rank clients identically, so both
have 71.3% accuracy. The overconfident one says "over 90%" for 15% of
clients and is right only 79% of the time; its log loss is 0.76 against
0.56 for the calibrated model.
[`u8_proper_scoring.py`](../05-illustrations/u8_proper_scoring.py)

**Regulatory hook.** SR 26-2. **NIST AI RMF.** MEASURE 2.5.

## How the tests fit together

U1 sets the yardstick (expected harm). U8 ensures the probabilities behind
decisions are honest. U2 uses both to decide when not to decide. U4 to U7
widen the same idea to individual recommendations, model choice, inputs and
changes over time.
