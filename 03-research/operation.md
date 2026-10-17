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

**Data.** The scoring model and a representative client sample.

**Method.**
1. Neutralise each input in turn by setting it to its median.
2. Measure the share of recommendations that change.
3. Compare with an agreed maximum.

**Setting the pass criteria.** No single input changes more than an agreed
share of recommendations (here 30%), or the dependence is justified and the
input gets extra controls.

**What the illustration shows.** In a stand-in scoring rule, question 1 (how
the client would react to a 20% fall) carries 45% of the weight and changes
49% of recommendations when neutralised. Age (20% weight) changes 18%; each of
the other questions about 7%.
[`o1_single_feature_dominance.py`](../05-illustrations/o1_single_feature_dominance.py)

**Regulatory hook.** SR 26-2. **NIST AI RMF.** MEASURE 2.5.

---

### O2. Champion and challengers

**Objective, method and pass criteria.** Build at least two structurally
different challengers for the same task (for example, a rules-based mapping
and a statistical model) and document why the champion is preferred, using
the agreed metrics (U1 expected cost, F and G fairness results). Pass if a
signed comparison exists and is refreshed on an agreed schedule.

**Client harm.** The model in use was never compared with simpler or
different alternatives that might serve clients better.

**Regulatory hook.** SR 26-2 (benchmarking, under conceptual soundness). **NIST AI RMF.** MEASURE 2.13. Related: D6, U5.

### O3. Shadow challenger

**Objective, method and pass criteria.** Run a retrained challenger in
shadow on live inputs, without acting on it, and compare continuously. Pass
if sustained outperformance is escalated within an agreed time.

**Client harm.** A better model exists but nobody checks, so clients keep
receiving advice that could be improved.

**Regulatory hook.** SR 26-2 (ongoing monitoring). **NIST AI RMF.** MEASURE 2.4.

## How the tests fit together

O1 is a robustness check on the model as built. O2 justifies the choice at
approval. O3 keeps the justification current.
