# Organising the validation with the NIST AI RMF

> Function and subcategory descriptions are paraphrased from NIST AI 100-1
> (2023); see [SOURCES.md](../SOURCES.md).

## Why use it

The regulations say what models used in advice must deliver for clients.
SR 26-2, which replaced SR 11-7 in April 2026, says how a model should be
validated. Neither sets out how to evidence the properties now expected of AI
systems, such as fairness, explainability and resilience, and SR 26-2 leaves
generative and agentic AI out of scope altogether. The NIST AI Risk Management
Framework fills that space. It is voluntary, but
it gives a shared structure that compliance, model owners and validators can
all work to.

It has four functions. **GOVERN** is cross-cutting: policies,
accountability and culture. **MAP** establishes context: what the system is
for, who it affects and which risks follow. **MEASURE** analyses and tracks
those risks. **MANAGE** prioritises and acts on what the measurements find.

## How each function shaped this work

### GOVERN: deciding the rules before testing

- Pass criteria, cost matrices, comparison groups and materiality thresholds
  are agreed with the model owner **before** any test runs, and dated. This
  repository never prescribes a tolerance; it shows how to set one.
- Results are labelled confirmatory or exploratory
  ([F7](../03-research/fair-treatment.md)).
- Triggers for independent outside review are written down
  ([F10](../03-research/fair-treatment.md)).

### MAP: from obligations to risks

- The [regulatory map](../01-regulation/regulatory-map.md) sets out what the
  rules require of the models, and [the gaps](../01-regulation/gaps-and-enforcement.md)
  show where a standard validation would have no evidence.
- Each test in the [catalogue](../04-test-design/catalogue.md) starts from a
  named harm to a client, not from a statistical property.
- Which changes in the world could break the model is written down in advance
  ([R2](../03-research/shift-and-dependence.md)).

### MEASURE: where most of the work sits

Every test carries the MEASURE subcategory it evidences. The table shows how
the 50 tests are spread.

| Subcategory | What NIST asks for (paraphrased) | Tests |
|---|---|---|
| MEASURE 1.3 | Assessments involve experts independent of the developers | F10 |
| MEASURE 2.1 | Test sets, metrics and tools are documented | D7, F8 |
| MEASURE 2.3 | Performance is demonstrated in conditions like deployment | F9, G5, R3 |
| MEASURE 2.4 | Behaviour is monitored in production | D3, U7, O3 |
| MEASURE 2.5 | The system is shown to be valid and reliable, and limits of generalisation are documented | D1, D2, D5, P1, P2, P3, P5, U8, S1, S4, S5, R1, R5, O1 |
| MEASURE 2.6 | Safety risks are evaluated and residual risk is within tolerance | D4, P4, U1 |
| MEASURE 2.8 | Transparency and accountability risks are examined | G4 |
| MEASURE 2.9 | The model is explained and its output interpreted in context | U4, U6, S3 |
| MEASURE 2.11 | Fairness and bias are evaluated and results documented | U3, F1 to F6, G1, G2, G3, G6, C1 |
| MEASURE 2.13 | The measurement methods themselves are evaluated | D6, U5, F7, S2, O2 |
| MEASURE 3.1 | Emerging risks are tracked in deployment | R4 |
| MAP 2.3 | Scientific integrity and test design considerations are documented | R2 |
| MANAGE 2.4 | Mechanisms exist to supersede or disengage the system | U2 |

Two subcategories carry most of the weight: validity and reliability (2.5)
and fairness (2.11). That matches where client harm from these models
is most likely: numbers that do not hold, and clients treated unequally.

### MANAGE: what happens to a result

- Each failed test becomes a finding with a severity, an owner, a remediation
  and a re-test date.
- Some tests are themselves management controls. Referral to a human
  ([U2](../03-research/decisions-under-uncertainty.md)) supersedes the model
  when it is unsure. Input drift ([D3](../03-research/data-fitness.md)) and
  shadow challengers ([O3](../03-research/operation.md)) trigger re-validation.

## Trustworthy characteristics and the tests that evidence them

| NIST characteristic | Example risk | Tests |
|---|---|---|
| Valid and reliable | Disclosed risk bands that do not hold; backtests nobody could achieve | P1 to P5, D1, D2, S1, R1 |
| Safe | A retiree's savings run out; a cautious client placed too aggressively | P4, D4, U1, U2 |
| Secure and resilient | One faulty input changes advice for many clients | O1 (security of AI agents is covered in the companion LLM repository) |
| Accountable and transparent | Aggregates reported without breakdowns; exploratory results presented as tests | G4, F7, F10 |
| Explainable and interpretable | "Drivers" disclosed to clients that a slightly different sample would not select | S3, U4, U6 |
| Privacy-enhanced | Client data flowing to third-party models | Covered in the companion LLM repository |
| Fair, with harmful bias managed | Proxy effects, badly served subgroups, unreliable measurement for some clients | F1 to F10, G1 to G6, U3, C1 |
