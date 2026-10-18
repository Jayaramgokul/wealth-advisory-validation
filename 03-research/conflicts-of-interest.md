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

**Data.** For each recommendation:
- **the sleeve** of the portfolio where the product choice is made, such as
  the core equity holding, and its share of the account;
- **every product eligible for that sleeve,** with its costs, its mandate and
  whether the firm or an affiliate owns or earns from it;
- **the product chosen;**
- **the client segment,** such as account size, channel or region, since a
  conflict can sit in one segment only;
- **the disclosure** the client received about own-brand products.

**Method.**
1. **Define a product-neutral benchmark:** what a ranking on cost and
   mandate fit, blind to who owns the product, would choose for each sleeve.
   The benchmark is agreed with compliance before the data is examined. Here
   the own-brand fund would be chosen for 10% of sleeves.
2. **Compute the own-brand share per segment,** with a 95% Wilson interval,
   and test it against the benchmark. A one-sided test is appropriate, since
   the concern is selection *above* the benchmark.
3. **Put a cost on the excess:** the share above the benchmark, times the
   average amount in the sleeve, times the fee difference between the
   own-brand product and the cheapest equivalent. Express it per client per
   year, which is what a client would understand.
4. **Look for the rule that causes it.** A tilt confined to one segment
   usually traces to a specific rule, such as a different product list for
   larger accounts.
5. **Read the disclosure** and ask whether a client could tell, from it, that
   this happens to them and what it costs.

**Setting the pass criteria.** Two conditions, agreed in advance:
- **No unexplained excess over the benchmark in any segment.** A difference
  can be statistically significant and still trivial in cost, so the bar
  combines both: significant *and* above an agreed cost per client.
- **Any excess that remains has a documented client-interest reason** (for
  example, a mandate no other product offers) and a disclosure specific
  enough for informed consent.

**What the illustration shows.** The script simulates 8,000 clients in three
account-size segments. In 40% of each account, the model chooses between an
own-brand fund (0.45% a year) and an equivalent outside fund (0.10%). A
product-neutral ranking would pick the own-brand fund 10% of the time, but
the simulated model has a rule that favours it for the largest accounts.

| Segment | Clients | Own-brand share (95% interval) | Test against 10% | Extra fees per client per year |
|---|---|---|---|---|
| Smaller (up to $25,000) | 4,009 | 10% (9–11%) | not significant | about $0 |
| Mid-size ($25,000 to $100,000) | 2,813 | 12% (11–14%) | significant | about $2 |
| Largest ($100,000 to $1 million) | 1,178 | **53%** (51–56%) | highly significant | **about $327** |

Across all clients, the own-brand share is 17%. On its own, that might pass
as a modest tilt. Segment by segment, the picture is clear: smaller accounts
match the benchmark, and the largest accounts are placed in the own-brand
fund more than half the time, at a cost of over $300 a year each. The
mid-size result shows why the criteria combine significance and cost: a
2-point excess is statistically significant with 2,800 clients but costs
about $2 a year.
[`c1_proprietary_product_tilt.py`](../05-illustrations/c1_proprietary_product_tilt.py)

**Adjacent tests.**
- **R4** watches for feedback loops: a tilt in recommendations can reshape
  the data future models learn from.
- **F3** uses the same segment-by-segment logic for suitability; a conflict,
  like unfairness, can hide in an average.
- **P2** applies the same caution to claims that one product performs better
  than another.

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
