# The model in operation

> Public sources only; full references in [SOURCES.md](../SOURCES.md). Every
> number quoted below comes from the simulated data in
> [05-illustrations](../05-illustrations/), not from any real firm.

## Why this lens

The *Companion to the Model AI Governance Framework* (World Economic Forum
with Singapore's IMDA and PDPC) is a practical guide to running AI
responsibly across its life cycle. Two of its themes matter most for models
used in advice once they are live: whether the model was **chosen for good
reasons over alternatives**, and whether it is **robust**, so that one bad
input does not change advice for many clients at once. SR 26-2 points the
same way with benchmarking and ongoing monitoring.

## What I read, and what each source changed

| Source | The idea I took from it | What it changed in the tests |
|---|---|---|
| WEF, IMDA & PDPC (2020), *Companion to the Model AI Governance Framework* | Document why a model was selected and how robust it is; keep checking it in operation. | Single-input dominance (O1); champion and challengers (O2); shadow challenger (O3) |
| SR 26-2 (2026) | Benchmarking to other models is one way to assess conceptual soundness; monitoring continues after approval. | O2 and O3 |

## The tests

---

### O1. Single-feature dominance

**Principle.** A model whose decisions hinge on one input inherits every
weakness of that input: a misread question, a form change, a broken feed.

**Objective.** Measure each input's actual influence on recommendations, not
its stated weight.

**Client harm.** One faulty field changes the advice for a large share of
clients at the same time.

**Why existing tests miss it.** Reviews read the documented weights. The
influence of an input also depends on its spread and on where clients sit
relative to bucket boundaries.

**Data.**
- **The scoring model,** in a form the validator can run on edited inputs.
- **A representative sample of real clients,** since an input's influence
  depends on how clients' answers are actually spread, which synthetic data
  may not capture.
- **The documented weight of each input,** to compare with its actual
  influence.

**Method.**
1. **Neutralise each input in turn,** setting it to its median for every
   client while leaving all other inputs unchanged.
2. **Measure the share of recommendations that change,** compared with the
   unedited run.
3. **Compare with an agreed maximum,** and with the documented weights. An
   input whose influence is far larger than its weight suggests is a finding
   in itself.
4. **Repeat for realistic failures** of the most influential inputs, not
   only the median: the question left blank, its answers reversed by a form
   change, or the field defaulting to a fixed value.

**Setting the pass criteria.** No single input changes more than an agreed
share of recommendations (here 30%). Where one does, either its dominance is
justified, for example because it is the most direct question about risk,
or the input gets extra controls: validation checks on the answer, a
follow-up question when it contradicts the others, and monitoring for sudden
changes in its distribution (D3).

**What the illustration shows.** The script applies a stand-in scoring rule
to 6,000 simulated clients. Question 1, which asks how the client would react
to a 20% fall, carries 45% of the weight; age carries 20%; each of the seven
other questions carries 5%.

| Input | Weight | Recommendations that change when it is set to its median |
|---|---|---|
| Question 1 (reaction to a 20% fall) | 0.45 | **49.2%** |
| Age | 0.20 | 18.0% |
| Each of questions 2 to 8 | 0.05 | 6.3% to 7.1% |

Setting question 1 to its median changes the recommendation for about half
of all clients, above the 30% limit. A misread wording, a form change that
reverses its scale, or a default value in a broken feed would move half the
book at once. The other inputs stay well within the limit. The weights alone
would not reveal this: 0.45 does not obviously mean "half of all
recommendations".
[`o1_single_feature_dominance.py`](../05-illustrations/o1_single_feature_dominance.py)

**Adjacent tests.**
- **F1** uses the same edit-and-rerun approach for attributes that should
  not matter at all.
- **F5** checks how reliably each question measures risk tolerance; a
  dominant question that is also unreliable is the worst combination.
- **S3** checks that the inputs described as drivers are stable.

**Regulatory hook.** SR 26-2. **NIST AI RMF.** MEASURE 2.5.

---

### O2. Champion and challengers

**Objective.** Show that the model in use (the "champion") was chosen over
structurally different alternatives for documented reasons, and keep that
comparison current.

**Client harm.** The model in use was never compared with simpler or
different alternatives that might serve clients better.

**Why existing tests miss it.** A model is usually compared with its own
previous version, which shares its assumptions and its blind spots.

**Data.** The same validation data for the champion and at least two
challengers, and the metrics the firm has agreed to judge models on.

**Method.**
1. **Build at least two structurally different challengers** for the same
   task, for example a rules-based mapping from answers to bands, and a
   statistical model of a different family from the champion's.
2. **Compare them on the agreed metrics:** expected cost (U1), the direction
   of errors (G2), and the fairness results (F2 to F4), with intervals.
3. **Look at where they disagree,** and which model is right in those cases
   against the reference labels.
4. **Document why the champion is preferred,** including what it gives up.
   A simpler challenger that performs about as well is a strong argument for
   simplicity (D6).

**Setting the pass criteria.** Pass if a signed comparison exists, the
champion is not clearly worse than any challenger on the agreed metrics, and
the comparison is refreshed on an agreed schedule or after any material
change.

**Adjacent tests.**
- **D6** compares the model with naive baselines; O2 with serious
  alternatives.
- **U5** looks at close candidates from development; O2 keeps challengers
  in view after approval.
- **R5** uses a flexible challenger to find where the champion's shape is
  wrong.

**Regulatory hook.** SR 26-2 (benchmarking, under conceptual soundness). **NIST AI RMF.** MEASURE 2.13.

### O3. Shadow challenger

**Objective.** Run a challenger on live inputs alongside the model, without
acting on its output, so that a better model is noticed when it appears.

**Client harm.** A better model exists but nobody checks, so clients keep
receiving advice that could be improved.

**Why existing tests miss it.** Once a model is approved, comparisons
usually stop until the next scheduled review, which may be a year or more
away.

**Data.** Live inputs, the champion's outputs, the challenger's outputs on
the same inputs, and outcomes or reference labels as they become available.

**Method.**
1. **Retrain a challenger regularly** on recent data and run it in shadow on
   every live case, recording its output but never acting on it.
2. **Compare continuously** on the agreed metrics, as outcomes arrive.
3. **Escalate sustained outperformance,** meaning a lead that persists over
   an agreed period and survives its interval, not a single good month.
4. **Look at disagreements as they happen.** Cases where the two models
   disagree sharply are worth a human look, whichever turns out right.

**Setting the pass criteria.** Pass if the shadow challenger runs
continuously, comparisons are reported on schedule, and sustained
outperformance is escalated to the model owner within an agreed time.

**Adjacent tests.**
- **O2** sets up the comparison at approval; O3 keeps it running.
- **D3** shows when the population has shifted, which is often when a
  challenger starts to win.

**Regulatory hook.** SR 26-2 (ongoing monitoring). **NIST AI RMF.** MEASURE 2.4.

## How the tests fit together

O1 is a robustness check on the model as built. O2 justifies the choice at
approval. O3 keeps the justification current.
