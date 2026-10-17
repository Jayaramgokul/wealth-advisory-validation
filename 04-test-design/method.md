# How the tests were derived

## Why go beyond a standard checklist

A standard model validation asks about data quality, conceptual soundness,
outcomes and monitoring. That is necessary but not enough for models that
profile clients, place them and describe their risk: it does not say how to show that clients are treated alike, that
risk disclosures hold in a crash, or that a firm's own products are not
quietly favoured. Research has already studied those failures and designed
ways to detect them, so the tests here come from reading that research as a
set of lenses.

## One source, one lens

Each source was read with the same question: *if this is right, what would
an existing validation miss?* Each answer became a candidate test.

| Lens | Source | Question |
|---|---|---|
| [The data](../03-research/data-fitness.md) | Gebru et al., *Datasheets for Datasets*; Elton, Gruber & Blake; DeMiguel et al.; Cohen | Is the data fit for the decisions the model makes? |
| [Portfolio risk and performance](../03-research/portfolio-risk-and-performance.md) | Artzner et al.; Rockafellar & Uryasev; Sharpe; Sortino & Price; Lo; RiskMetrics; Bengen; Efron | Do the numbers shown to clients hold up when measured more than one way? |
| [Decisions under uncertainty](../03-research/decisions-under-uncertainty.md) | Bishop, *Pattern Recognition and Machine Learning*; Gneiting & Raftery | Are the costs of different mistakes weighed, and does the model know when to refer? |
| [Fair treatment](../03-research/fair-treatment.md) | Barocas et al.; Kusner et al.; EEOC guidelines; Grable & Lytton | Are clients treated alike when they should be, and are the fairness tests well designed? |
| [Groups an average hides](../03-research/groups-an-average-hides.md) | Buolamwini & Gebru, *Gender Shades*; Barocas et al. | Can a good average hide a badly served group? |
| [Conflicts](../03-research/conflicts-of-interest.md) | SEC order against SoFi Wealth (2021); IA-5248 | Are own-brand products favoured? |
| [Statistical rigour](../03-research/statistical-rigour.md) | Hastie, Tibshirani & Friedman; Benjamini & Hochberg; Meinshausen & Bühlmann | Are results honest about variance and multiple testing? |
| [Shift and dependence](../03-research/shift-and-dependence.md) | Saria & Subbaswamy; Künsch | What changes would break the model, and are intervals valid for dependent data? |
| [Operation](../03-research/operation.md) | WEF *Companion*; SR 26-2 | Is the model fragile to one input, and was it chosen over alternatives for good reason? |

## What every test entry contains

The principle from the source; the objective in plain language; the harm to
the client; why existing tests miss it; the data needed; the method; pass
criteria agreed *before* testing; and how it relates to neighbouring tests.

## Three disciplines

1. **No duplicates.** Each candidate is checked against existing tests;
   overlaps are merged or framed as complements.
2. **Decide the bar before looking.** Pass criteria and comparison groups are
   fixed in advance; anything chosen after seeing the data is exploratory.
3. **Count the tests.** Results are reported with the false discovery rate
   controlled across the whole suite ([S2](catalogue.md)).

## From a test to an illustration

Where a test can be shown on simulated data, there is a short standalone
script in [05-illustrations](../05-illustrations/). Each one states the
question, applies the method exactly as written in the research document, and
prints what the result means in plain language. The scripts show the method;
they are not a model of any real firm or system.
