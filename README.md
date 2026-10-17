# Investment & Wealth Management Advisory Validation

![tests](https://github.com/Jayaramgokul/wealth-advisory-validation/actions/workflows/tests.yml/badge.svg)
![python](https://img.shields.io/badge/python-3.10%2B-blue)
![licence](https://img.shields.io/badge/licence-MIT-green)

**How I approach the independent validation of models used in investment
and wealth management (risk profiling, suitability and portfolio risk): what
the regulations require, where a standard model review falls
short, what the research says about testing those gaps, and how each test is
designed.**

> Draws on my experience validating AI and quantitative models in financial
> services. All examples use public sources and synthetic data.

This is a validator's notebook, not software. The documents carry the
argument; the short Python scripts show individual methods working on
simulated data.

## The reasoning, in order

```
01 Regulation        What do the rules require of these models, and which obligations does a standard review not test?
        │
        ▼
02 NIST AI RMF       How the work is organised: govern, map, measure, manage
        │
        ▼
03 Research          What has the literature already learned about testing each gap?
        │
        ▼
04 Test design       Objective, client harm, data, method, pass criteria, NIST subcategory, regulatory hook
        │
        ▼
05 Illustrations     Each method on simulated data, with its result explained in plain language
```

| Step | Read |
|---|---|
| 1. Obligations | [Regulatory map](01-regulation/regulatory-map.md): fiduciary duty, SEC IM Guidance 2017-02, FINRA, Marketing Rule, retirement and senior-investor rules, SR 26-2 |
| | [Gaps and enforcement](01-regulation/gaps-and-enforcement.md): areas a standard validation misses, in three pillars; SoFi Wealth, the 2024 AI-washing cases, exam priorities |
| 2. Framework | [NIST AI RMF](02-nist-ai-rmf/nist-ai-rmf.md): how each function shaped the work, and which tests evidence which subcategory |
| 3. Research | [Portfolio risk and performance](03-research/portfolio-risk-and-performance.md): tail risk, risk-adjusted returns, volatility estimators, sequence risk, intervals |
| | [Fair treatment of clients](03-research/fair-treatment.md): counterfactual twins, adverse impact with power, intersectional groups, adjusted disparity, questionnaire reliability |
| | [Groups an average hides](03-research/groups-an-average-hides.md): direction of errors, thresholds, reporting standards |
| | [Placing clients under uncertainty](03-research/decisions-under-uncertainty.md): asymmetric costs, referral to a human, proper scoring |
| | [The data underneath the model](03-research/data-fitness.md): survivorship, look-ahead, drift, stressed correlations, label reliability |
| | [Conflicts of interest](03-research/conflicts-of-interest.md): own-brand product tilt against a neutral benchmark |
| | [Statistical rigour](03-research/statistical-rigour.md): nested cross-validation, multiple testing, selection stability |
| | [Reliability when the world shifts](03-research/shift-and-dependence.md): dependent data, shift, feedback loops |
| | [The model in operation](03-research/operation.md): single-input dominance, challengers |
| 4. Method | [How the tests were derived](04-test-design/method.md): one source, one lens, three disciplines |
| 5. Catalogue | [All 50 tests](04-test-design/catalogue.md), each with its risk, method, pass criteria, NIST AI RMF subcategory and regulatory hook |
| 6. Illustrations | [05-illustrations](05-illustrations/): 26 standalone scripts, one per test that can honestly be shown on simulated data |
| Sources | [SOURCES.md](SOURCES.md): every regulation and paper cited, with links |

## A few things the illustrations show

| Test | On simulated data |
|---|---|
| [P1 Tail risk, three ways](05-illustrations/p1_tail_risk_three_ways.py) | A normal model puts the worst-month average loss of an aggressive portfolio at 11.5%; the actual tail is 15.2% |
| [P4 Sequence of returns](05-illustrations/p4_sequence_of_returns.py) | The same returns in a different order exhaust the aggressive portfolio in 24% of cases over 30 years |
| [D3 Input drift](05-illustrations/d3_input_drift_psi.py) | The client base shifts sharply in age and experience while the recommended mix barely moves |
| [U1 Cost of mistakes](05-illustrations/u1_cost_of_mistakes.py) | The more accurate of two models is worse for clients, because its errors lean towards too much risk |
| [F2 Adverse impact with power](05-illustrations/f2_adverse_impact_four_fifths.py) | A group of 60 clients "passes" the four-fifths rule but is too small to detect an 18-point gap, so it is inconclusive |
| [F3 Intersectional groups](05-illustrations/f3_worst_group_intersectional.py) | No single factor costs more than 8 points; one combination is 17 points below average |
| [C1 Proprietary product tilt](05-illustrations/c1_proprietary_product_tilt.py) | A tilt confined to large accounts costs those clients about $330 a year, while the overall share looks modest |
| [S2 Multiple testing](05-illustrations/s2_multiple_testing.py) | 300 segment tests at p < 0.05 raise 6 false alarms; controlling the false discovery rate removes them |

![Suitability by client group, with intervals](05-illustrations/output/f3_intersectional.png)

## Run the illustrations

```bash
git clone https://github.com/Jayaramgokul/wealth-advisory-validation.git && cd wealth-advisory-validation
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python 05-illustrations/p1_tail_risk_three_ways.py     # any script; charts go to 05-illustrations/output/
python -m pytest tests/ -q                            # checks the shared statistics and runs every script
```

## Limitations

All data is simulated, so the numbers illustrate methods, not any real firm.
The "true" risk tolerance used in some scripts exists only because the data
is simulated. Thresholds shown are examples; in a real validation they are
agreed with the model owner before testing. Regulations are summarised, not
quoted, and their current status should be checked before relying on them.

## Licence

MIT.
