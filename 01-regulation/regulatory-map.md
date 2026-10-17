# What the rules require of models used in investment advice

> Public sources only; see [SOURCES.md](../SOURCES.md). Rules are summarised,
> not quoted; check their current status before relying on them.

## First question: which rulebook applies?

Models used in investment advice and wealth management (risk profiling,
suitability, portfolio construction, risk disclosure) can sit inside an
investment adviser (Advisers Act), a broker-dealer (FINRA member), or both.
The answer decides which obligations a validation has to evidence, so it is
settled first rather than assumed.

## Core obligations and what they mean for the models

| Obligation | Source | What to test |
|---|---|---|
| **Duty of care:** advice in the client's best interest, based on a reasonable understanding of their objectives, with monitoring | SEC Release IA-5248 (2019) | Placements match the client's true tolerance ([U1](../03-research/decisions-under-uncertainty.md)); borderline clients are referred ([U2](../03-research/decisions-under-uncertainty.md)); the population and inputs are monitored ([D3](../03-research/data-fitness.md)) |
| **Duty of loyalty:** no subordinating clients to the firm; full and fair disclosure of conflicts | IA-5248; SEC order IA-5826 (SoFi Wealth, 2021) | Own-brand products are not favoured without disclosure ([C1](../03-research/conflicts-of-interest.md)) |
| **Questionnaire, disclosure, testing the algorithm** | SEC IM Guidance Update 2017-02 | The questionnaire measures reliably for every client ([F5](../03-research/fair-treatment.md)); inconsistent answers are caught; the algorithm is tested before and after launch |
| **Governance of algorithms, client profiling, rebalancing** | FINRA Report on Digital Investment Advice (2016) | Methodology review; ongoing output testing; handling contradictory profile answers |
| **Performance advertising** | SEC Marketing Rule 206(4)-1 | Backtested or hypothetical performance is fair and balanced; risk-adjusted claims survive intervals ([P2](../03-research/portfolio-risk-and-performance.md)); stated risk bands hold ([P1, P5](../03-research/portfolio-risk-and-performance.md)) |
| **Retirement accounts** | DOL PTE 2020-02; prohibited-transaction rules for IRAs | Retirement-specific advice logic; decumulation risk ([P4](../03-research/portfolio-risk-and-performance.md)) |
| **Senior and vulnerable clients** | FINRA Rules 2165 and 4512; state adoptions of the NASAA model act | Older-client outcomes reported separately ([F3](../03-research/fair-treatment.md)); referral to a human when unsure ([U2](../03-research/decisions-under-uncertainty.md)) |
| **Fair treatment** | Fiduciary duty; anti-discrimination principles | No proxy effects ([F1, F2, F4](../03-research/fair-treatment.md)); worst group reported ([F3](../03-research/fair-treatment.md)); direction of errors ([G2](../03-research/groups-an-average-hides.md)) |
| **Model risk management** | SR 26-2 (Federal Reserve, OCC and FDIC, April 2026; replaced SR 11-7) | Inventory, documentation, effective challenge with independence, conceptual soundness, outcomes analysis, ongoing monitoring, all scaled to model materiality; estimator choices justified ([P3](../03-research/portfolio-risk-and-performance.md)) |

SR 26-2 is written for banking organisations; advisers and broker-dealers
commonly apply its principles as best practice. It scales the rigour of
validation to a model's materiality, which is one reason every pass criterion
here is agreed with the model owner rather than fixed in advance by this
repository.

Registration and client-asset rules also apply to any adviser. They are
checked by process review rather than by testing a model, so they are not
developed here.

## Three pillars

Validations of these models tend to be strongest on suitability and
quantitative testing, weaker on conflicts, and weakest on governance. The gap
areas, and the enforcement actions that shaped priorities, are set out in
[gaps and enforcement](gaps-and-enforcement.md). This repository covers the
first two pillars in depth; the governance side of AI systems (vendors,
change control, complaints, continuity, privacy) is the subject of a
companion repository on LLM agent validation.
