# Conflicts of interest

> Public sources only; full references in [SOURCES.md](../SOURCES.md). Every
> number quoted below comes from the simulated data in
> [05-illustrations](../05-illustrations/), not from any real firm.

## Why this lens

The duty of loyalty requires an adviser not to place its own interests ahead
of its clients', and to disclose conflicts fully and fairly enough for
informed consent (SEC Release IA-5248). With human advice, a conflict
shows up in individual recommendations. With a model, it can
sit in a single rule applied to thousands of accounts. It may affect only
some of them, so the overall figures look modest.

This is not hypothetical. In 2021 the SEC found that SoFi Wealth
breached its fiduciary duty in connection with moving client
assets into its own ETFs without adequately disclosing the conflict,
and it paid a $300,000 penalty (Release IA-5826). The test below is designed
to find that pattern in data before an examiner does.

## What I read, and what each source changed

| Source | The idea I took from it | What it changed in the tests |
|---|---|---|
| SEC Release IA-5248 (2019) | Duty of loyalty: no subordinating client interests; disclosure specific enough for informed consent. | The pass criterion covers disclosure quality, not only the tilt |
| SEC order against SoFi Wealth (2021), IA-5826 | Model-driven product choice can carry a firm's conflict at scale. | Compare own-brand share with a product-neutral benchmark (C1) |
| SEC order against SoFi Wealth (2021) | Conflicts can affect some clients and not others. | Test segment by segment, not only overall |

## The test

### C1. Proprietary product tilt

**Principle.** If the firm's own product is chosen more often than a
product-neutral rule would choose it, the difference needs a client-interest
reason or a specific disclosure.

**Objective.** Measure how often the own-brand product is selected compared
with a neutral benchmark, by client segment, and put a cost on any excess.

**Client harm.** Clients pay higher fees for an equivalent exposure, often
without knowing a choice was made for them.

**Why existing tests miss it.** Suitability testing checks that each
portfolio fits the client. A portfolio holding the own-brand fund can be
perfectly suitable and still cost more than an equivalent one.

**Data.** For each recommendation: the sleeve, the products eligible for it,
their costs and mandates, the product chosen, and the client segment.

**Method.**
1. Define a product-neutral benchmark: what a ranking on cost and mandate
   fit, blind to ownership, would choose. Here the own-brand fund would be
   chosen for 10% of sleeves.
2. Share of own-brand selections per segment, with Wilson intervals and a test
   against the benchmark.
3. The fee difference on the excess, per client per year.
4. Read the disclosure and ask whether a client could tell, from it, that
   this happens and what it costs.

**Setting the pass criteria.** No unexplained excess over the benchmark in
any segment. Any excess has a documented client-interest reason and a
disclosure specific enough for informed consent.

**What the illustration shows.** Small and mid-size accounts are close to the
benchmark (10% and 12%). The largest accounts are placed in the own-brand fund
53% of the time, costing roughly $330 per client a year in extra fees. The
overall share, diluted by the smaller accounts, would look much less striking.
[`c1_proprietary_product_tilt.py`](../05-illustrations/c1_proprietary_product_tilt.py)

**Adjacent tests.** R4 (feedback loops), because a tilt in recommendations can
reshape the data future models learn from.
**Regulatory hook.** Duty of loyalty (IA-5248); SEC order IA-5826 (SoFi
Wealth, 2021). **NIST AI RMF.** MEASURE 2.11.

## Related enforcement: claims about AI

The conflict above concerns what the model recommends. A second line of
enforcement concerns what firms *say* about their technology. In 2024 the SEC
settled charges against two advisers, Delphia and Global Predictions, for
false and misleading statements about their use of AI (press release
2024-36). For a validator, that turns marketing claims about the model ("uses
machine learning on your data", "AI-driven") into statements to check against
the model documentation. Those checks are covered in the companion repository
on LLM agent validation.
