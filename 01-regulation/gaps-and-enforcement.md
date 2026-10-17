# Where standard validations fall short, and what regulators have acted on

> Public sources only; see [SOURCES.md](../SOURCES.md). Rules are summarised,
> not quoted; check their current status before relying on them.

## How the gaps were found

The [regulatory map](regulatory-map.md) lists what the rules require of
models used in investment advice. To find the gaps, I set each obligation against what a standard
model validation actually examines: data, conceptual soundness, outcomes and
monitoring, mostly for the suitability model. Anything an examiner could ask
about that the validation would not have evidence for became a gap area.

The areas fell into three pillars. Validations tend to be strongest on the
first, weaker on the second, and weakest on the third. Pillar B repeats
conflicts in product selection, a core obligation rather than a gap, because
enforcement has focused on it.

## Pillar A: suitability and client protection

| Area | Public rules | Why it matters for the models | What to test | Covered in |
|---|---|---|---|---|
| **Retirement accounts** | DOL PTE 2020-02; prohibited-transaction rules for IRAs | Retirement advice, including rollovers, carries its own best-interest conditions | Does the model recognise the account type and change its logic? Is decumulation risk tested? | [P4](../03-research/portfolio-risk-and-performance.md) |
| **Senior and vulnerable clients** | FINRA Rules 2165 and 4512; state adoptions of the NASAA model act | Recommending volatile strategies to an older client without safeguards is a recurring examination concern | Older-client outcomes reported separately; trusted-contact capture; referral to a human when unsure | [F3](../03-research/fair-treatment.md), [U2](../03-research/decisions-under-uncertainty.md) |
| **Advertising and communications** | SEC Marketing Rule 206(4)-1; FINRA Rule 2210 | Backtested performance and risk claims must be fair, balanced and substantiated; claims about the technology itself are a new focus (see below) | Risk bands that hold; rankings that survive intervals; backtests free of survivorship and look-ahead bias | [P1, P2, P5](../03-research/portfolio-risk-and-performance.md), [D1, D2](../03-research/data-fitness.md) |

## Pillar B: conflicts of interest

| Area | Public rules | Why it matters for the models | What to test | Covered in |
|---|---|---|---|---|
| **Conflicts in product selection** | Duty of loyalty (IA-5248) | A conflict can sit in one rule applied to thousands of accounts | Own-brand share against a product-neutral benchmark, by segment, with cost | [C1](../03-research/conflicts-of-interest.md) |

## Pillar C: governance and controls

These areas concern the system around the model more than the model itself,
and matter most where a language model is part of the system. They are developed in the companion repository on LLM agent
validation.

| Area | Public rules |
|---|---|
| Third-party and model-vendor risk | Interagency Guidance on Third-Party Relationships (2023); SR 11-7 |
| Model inventory and documentation | SR 11-7; NIST AI RMF |
| Change management | SR 11-7 |
| Complaints received through a chat interface | FINRA Rules 4513, 4530 and 3110 |
| Business continuity | FINRA Rule 4370; Compliance Rule 206(4)-7 |
| Privacy | Regulation S-P (2024 amendments) |
| Financial crime controls | Bank Secrecy Act and AML programme rules; OFAC sanctions |

## What regulators have acted on

Enforcement shows where supervisors have already looked. Three items shaped
the priorities in this repository.

| Action | What happened | What it means for validation |
|---|---|---|
| **SoFi Wealth (2021)**, SEC Release IA-5826 | SoFi Wealth breached its fiduciary duty in connection with moving client assets into its own ETFs without adequately disclosing the conflict; $300,000 penalty. | Model-driven product choice must be tested for tilt and disclosure, segment by segment ([C1](../03-research/conflicts-of-interest.md)). |
| **Delphia and Global Predictions (2024)**, SEC press release 2024-36 | Two advisers settled charges over false and misleading statements about their use of artificial intelligence; $400,000 in penalties in total. | Claims about what the model does are statements of fact that need substantiation, so the validator checks them against the model documentation. |
| **SEC examination priorities** (published annually) | Algorithmic advice and the use of AI have been recurring themes. | Examiners will ask how a firm validated its models, so the evidence needs to exist before the examination. |

## Where the NIST AI RMF fits

The regulations say *what* must hold. The [NIST AI RMF](../02-nist-ai-rmf/nist-ai-rmf.md)
gave the structure for organising *how* to evidence it: governance and
context first, then measurement, then management of what the measurements
find.
