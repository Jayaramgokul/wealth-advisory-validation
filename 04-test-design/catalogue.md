# Test catalogue

*Generated from [catalogue.yaml](catalogue.yaml) by `render_catalogue.py`. Edit the YAML, not this page.*

50 tests in 9 groups. Each group reads one or more public sources as a lens and asks what an existing validation would miss. "Agreed tolerance" means a bar the validator and the model owner fix in advance; this repository does not prescribe one. Linked lenses have a full research write-up.

| Group | Lens | Question it asks | Tests |
|---|---|---|---|
| **D** | [The data underneath the model](../03-research/data-fitness.md) | Is the data the model learned from, and is tested on, fit for the decisions it now makes? | 7 |
| **P** | [Portfolio risk and performance](../03-research/portfolio-risk-and-performance.md) | Do the risk and return numbers shown to clients hold up when measured more than one way? | 5 |
| **U** | [Placing clients under uncertainty](../03-research/decisions-under-uncertainty.md) | Does the model weigh the different costs of different mistakes, and know when to refer a client to a human? | 8 |
| **F** | [Fair treatment of clients](../03-research/fair-treatment.md) | Are clients treated alike when they should be, and are the fairness tests themselves well designed? | 10 |
| **G** | [Groups an average can hide](../03-research/groups-an-average-hides.md) | Can a good average hide a group, or a combination of groups, that is badly served? | 6 |
| **C** | [Conflicts of interest](../03-research/conflicts-of-interest.md) | Do own-brand products get recommended more than the client's interest justifies? | 1 |
| **S** | [Statistical rigour](../03-research/statistical-rigour.md) | Are the reported numbers honest about variance, overfitting and multiple testing? | 5 |
| **R** | [Reliability when the world shifts](../03-research/shift-and-dependence.md) | Which changes in clients, markets or the model itself would break the model, and would anyone notice? | 5 |
| **O** | [The model in operation](../03-research/operation.md) | Is the chosen model justified against alternatives, and does it depend too much on one input? | 3 |

▶ marks tests with an illustration script in [05-illustrations](../05-illustrations/).

## D: [The data underneath the model](../03-research/data-fitness.md)

Is the data the model learned from, and is tested on, fit for the decisions it now makes?

| ID | Test | What goes wrong for the client | How to test | Passes if | NIST AI RMF | Regulatory hook |
|---|---|---|---|---|---|---|
| [D1 ▶](../05-illustrations/d1_survivorship_bias.py) | **Survivorship bias in backtest data** | Backtests built only on assets that still exist look better than any investor could have achieved. | Rebuild the historical universe including delisted or failed assets and compare backtest results with and without them. | Results on the full universe stay within the agreed tolerance of the published ones; the universe definition is documented. | MEASURE 2.5 | Marketing Rule (hypothetical performance) |
| [D2 ▶](../05-illustrations/d2_look_ahead_bias.py) | **Look-ahead bias and label leakage** | A feature uses information that was not available at decision time, so backtested skill is partly illusory. | Record the point-in-time availability of every feature; re-run the backtest with each feature lagged to when it was really known. | No material performance drop after point-in-time correction. | MEASURE 2.5 | SEC IM Guidance 2017-02 (testing the algorithm) |
| [D3 ▶](../05-illustrations/d3_input_drift_psi.py) | **Input drift, not just output drift** | The client population or market inputs move away from what the model was built on before outputs visibly change. | Compare the live distribution of each key input (age, account size, questionnaire answers, asset mix) with the reference snapshot using PSI or similar. (Population Stability Index; see Yurdakul 2018 on its statistical properties.) | Every key input is within the agreed drift band, or a drift alert has been raised and actioned. | MEASURE 2.4 | Duty of care (ongoing monitoring) |
| [D4 ▶](../05-illustrations/d4_stressed_correlation.py) | **Correlation breakdown under stress** | Diversification assumed from calm-market correlations disappears in a crash. | Recompute correlations over rolling and stress windows and re-run portfolio risk with stressed correlations. | Each portfolio stays within its disclosed risk band under stressed correlations. | MEASURE 2.6 | Duty of care (suitability) |
| D5 | **Out-of-distribution detection and abstention** | The model recommends assets or answers clients unlike anything in its data, with unearned confidence. | Define in-distribution criteria (history length, liquidity, profile ranges) and test that out-of-range cases are flagged or declined. | Out-of-range cases are flagged or routed to a human at the agreed rate. | MEASURE 2.5 | Duty of care |
| D6 | **Baseline value-add** | The model adds complexity and cost without beating simple rules. | Compare against naive baselines (equal weight, a static balanced mix, a market-cap rule) on the same data. | The model beats the baselines on risk-adjusted outcomes by a margin that survives resampling. | MEASURE 2.13 | Duty of care (best interest) |
| [D7 ▶](../05-illustrations/d7_rater_agreement.py) | **Label noise and rater agreement** | Training or evaluation labels (for example "suitable" or "risk tolerance") are inconsistent, so the model learns noise. | Have independent raters re-label a sample; measure agreement (Cohen's or Fleiss' kappa). | Agreement is above the agreed level for every label type. | MEASURE 2.1 | SR 26-2 (model testing of data quality and relevance) |

## P: [Portfolio risk and performance](../03-research/portfolio-risk-and-performance.md)

Do the risk and return numbers shown to clients hold up when measured more than one way?

| ID | Test | What goes wrong for the client | How to test | Passes if | NIST AI RMF | Regulatory hook |
|---|---|---|---|---|---|---|
| [P1 ▶](../05-illustrations/p1_tail_risk_three_ways.py) | **Tail risk, three ways** | A portfolio's disclosed loss band understates how bad a bad year can be. | Estimate VaR and CVaR by historical simulation, a parametric model and Monte Carlo; compare them and the disclosed band. | The methods agree within tolerance and the worst estimate stays inside the disclosed band. | MEASURE 2.5 | Disclosure; Marketing Rule (hypothetical performance) |
| [P2 ▶](../05-illustrations/p2_sharpe_sortino_intervals.py) | **Risk-adjusted returns with intervals** | Portfolios are ranked on Sharpe or Sortino ratios whose differences are noise. | Bootstrap the Sharpe and Sortino ratios of each portfolio and compare intervals. | Any claimed ranking holds across the bootstrap intervals. | MEASURE 2.5 | Marketing Rule (fair and balanced performance) |
| [P3 ▶](../05-illustrations/p3_ewma_vs_sample_volatility.py) | **Volatility estimator sensitivity** | The choice between an EWMA and an equal-weighted volatility estimate changes how much risk clients hold. | Run the same exposure rule with EWMA (lambda 0.94) and a one-year sample estimate; compare forecast error, band breaches and average exposure. | Outcomes differ by less than the pre-agreed materiality, or the choice is documented and justified. | MEASURE 2.5 | SR 26-2 (conceptual soundness) |
| [P4 ▶](../05-illustrations/p4_sequence_of_returns.py) | **Sequence-of-returns risk for retirees** | Two retirees with identical average returns run out of money at different times because of the order of returns. | Reorder the same historical returns many times and measure how often withdrawals deplete the portfolio. | Depletion probability for decumulating clients is within the agreed limit and disclosed. | MEASURE 2.6 | Duty of care; retirement accounts (DOL PTE 2020-02); senior investors |
| [P5 ▶](../05-illustrations/p5_intervals_on_risk_metrics.py) | **Confidence intervals on risk metrics** | A disclosed drawdown or volatility band is a single estimate that could easily be worse. | Block bootstrap of returns to put intervals on each portfolio's risk metrics. | The upper end of each interval stays inside the disclosed band, or the band is widened. | MEASURE 2.5 | Disclosure (SEC IM Guidance 2017-02); Marketing Rule |

## U: [Placing clients under uncertainty](../03-research/decisions-under-uncertainty.md)

Does the model weigh the different costs of different mistakes, and know when to refer a client to a human?

| ID | Test | What goes wrong for the client | How to test | Passes if | NIST AI RMF | Regulatory hook |
|---|---|---|---|---|---|---|
| [U1 ▶](../05-illustrations/u1_cost_of_mistakes.py) | **Asymmetric cost of mistakes** | Placing a cautious client in an aggressive portfolio is treated as no worse than the reverse. | Agree a cost matrix for misplacements and report expected cost, not just accuracy. | Expected cost is within the agreed limit and is the headline metric. | MEASURE 2.6 | Duty of care (suitability) |
| [U2 ▶](../05-illustrations/u2_refer_when_unsure.py) | **Abstain when unsure** | The model always answers, even when the client sits on a boundary where a wrong call is costly. | Use the model's probabilities and the cost matrix to define a refer-to-human region; measure how many clients fall in it. | A refer-to-human rule exists and borderline clients are routed to it. | MANAGE 2.4 | Duty of care; FINRA 2165 (vulnerable clients) |
| U3 | **Dependence on protected attributes** | Outputs depend on a protected attribute in ways a comparison of averages does not reveal. | Mutual information between each output and each protected attribute, with intervals and multiple-testing control. | No significant dependence, or a documented explanation. | MEASURE 2.11 | Fair treatment |
| U4 | **Intervals on individual recommendations** | "Allocate 28% to equities" is presented as exact when the model is uncertain. | Produce a predictive interval for each recommendation and check its calibration on held-out data. | Intervals are calibrated and used downstream. | MEASURE 2.9 | Disclosure |
| U5 | **Cost of committing to one model** | A single model was chosen when close alternatives disagree materially. | Compare candidate models' evidence and where their recommendations disagree. | The choice is justified where alternatives are close. | MEASURE 2.13 | SR 26-2 (conceptual soundness) |
| U6 | **Data-supported feature use** | The model relies on inputs the data does not support. | Refit with priors that switch off unsupported features (automatic relevance determination). | Unsupported features are removed or justified. | MEASURE 2.9 | SR 26-2 |
| U7 | **Detecting a change in the client** | A client's situation changes but their risk profile stays fixed at onboarding. | Model clients as moving between hidden states and test detection on labelled examples. | Changes are detected at the agreed rate with few false alarms. | MEASURE 2.4 | Duty of care (monitoring) |
| [U8 ▶](../05-illustrations/u8_proper_scoring.py) | **Proper scoring rules** | Probabilistic outputs are trained or judged on metrics that reward overconfidence. | Check that every probabilistic layer is trained and evaluated with a proper scoring rule (log loss, Brier). | Proper scoring rules throughout; recalibration only as clean-up. | MEASURE 2.5 | SR 26-2 |

## F: [Fair treatment of clients](../03-research/fair-treatment.md)

Are clients treated alike when they should be, and are the fairness tests themselves well designed?

| ID | Test | What goes wrong for the client | How to test | Passes if | NIST AI RMF | Regulatory hook |
|---|---|---|---|---|---|---|
| [F1 ▶](../05-illustrations/f1_counterfactual_twins.py) | **Counterfactual twin clients** | Changing a single protected attribute, with everything else fixed, changes the advice. | For each client, create twins that differ in one attribute only and compare recommendations. | Twins receive the same recommendation, within tolerance. | MEASURE 2.11 | Fair treatment |
| [F2 ▶](../05-illustrations/f2_adverse_impact_four_fifths.py) | **Adverse impact with honest statistics** | Groups are treated differently, or a small group is declared fair when it is too small to tell. | Four-fifths rule plus a chi-square test with confidence intervals; flag groups too small for adequate power. | No group falls below four-fifths with significance; underpowered groups are flagged, not passed. | MEASURE 2.11 | Fair treatment |
| [F3 ▶](../05-illustrations/f3_worst_group_intersectional.py) | **Intersectional disaggregation** | Single-factor checks pass while a combination (older and small account, say) is badly served. | Pre-register a limited grid of factor combinations and report outcomes for each, with intervals and multiple-testing control. | Every populated cell is within tolerance or has a remediation plan. | MEASURE 2.11 | Fair treatment; FINRA 2165 (senior investors) |
| [F4 ▶](../05-illustrations/f4_adjusted_disparity.py) | **Adjusted disparity** | A raw gap between groups is driven by legitimate factors, or a real gap is hidden by them. | Report each disparity both raw and after controlling for pre-agreed legitimate factors. | Both versions are reported side by side with intervals. | MEASURE 2.11 | Fair treatment |
| [F5 ▶](../05-illustrations/f5_questionnaire_reliability.py) | **Measurement validity across groups** | The risk questionnaire measures tolerance reliably for some groups and poorly for others. | Test-retest or internal-consistency reliability of the questionnaire per group. | Reliability is similar across groups, or the difference is disclosed and addressed. | MEASURE 2.11 | SEC IM Guidance 2017-02 (questionnaire design) |
| F6 | **Where in the pipeline does unfairness arise** | A disparity appears at the end but its source (questionnaire, scoring, portfolio, narration) is unknown. | Measure the same fairness metric after each stage of the pipeline. | Each disparity is traced to a stage. | MEASURE 2.11 | SR 26-2 (effective challenge) |
| F7 | **Confirmatory or exploratory** | Exploratory fairness checks are reported as if they were pre-planned pass/fail tests. | Classify every fairness test; confirmatory ones need a hypothesis written down before the data is seen. | Every result is labelled, and confirmatory claims have a dated pre-registration. | MEASURE 2.13 | SR 26-2 (documentation) |
| F8 | **Is the evaluation data fit for purpose** | Fairness conclusions rest on data with too few members of some groups or unknown origins. | A datasheet for every evaluation dataset; compare its composition with the live client base. | Datasheets exist and gaps are stated. | MEASURE 2.1 | SR 26-2 (data selection, under conceptual soundness) |
| F9 | **Fairness on real usage** | Synthetic test clients miss how real clients interact. | Periodic disaggregated evaluation on consented production data, reconciled with lab results. | Runs on schedule; differences from lab results are explained. | MEASURE 2.3 | Duty of care (monitoring) |
| F10 | **When to bring in outside review** | Internal evaluators miss what an outsider would see. | Agree written triggers for independent outside review. | Triggers are documented and followed. | MEASURE 1.3 | SR 26-2 (independence, under effective challenge) |

## G: [Groups an average can hide](../03-research/groups-an-average-hides.md)

Can a good average hide a group, or a combination of groups, that is badly served?

| ID | Test | What goes wrong for the client | How to test | Passes if | NIST AI RMF | Regulatory hook |
|---|---|---|---|---|---|---|
| [G1 ▶](../05-illustrations/f3_worst_group_intersectional.py) | **Worst group as co-headline** | A strong average is reported while one group fares far worse. | Report the worst-performing group alongside every aggregate figure. (Built into F3: the worst cell is reported beside the overall figure.) | Every aggregate has its worst group and gap beside it. | MEASURE 2.11 | Fair treatment |
| [G2 ▶](../05-illustrations/g2_direction_of_errors.py) | **Direction of errors by group** | Two groups have the same error rate but one is pushed too aggressive and the other too cautious. | A confusion matrix per group; compare over- and under-placement rates. | No group's errors lean one way beyond tolerance. | MEASURE 2.11 | Duty of care (suitability) |
| [G3 ▶](../05-illustrations/g3_threshold_sweep.py) | **Thresholds and who they affect** | A cut-off between risk buckets or between answer and refusal treats groups differently. | Sweep each threshold and plot outcomes by group. | The chosen threshold is justified against its subgroup impact. | MEASURE 2.11 | Duty of care |
| G4 | **Disaggregated reporting standard** | Aggregate numbers reach governance and clients without any breakdown. | A written minimum breakdown (age band, account size, region, experience) for every reported metric. | Audits find the standard followed. | MEASURE 2.8 | Disclosure; SR 26-2 |
| G5 | **Benchmark composition** | The validation set does not look like the client base, so results do not transfer. | Compare group shares in validation data with the live client base. | Shares match within tolerance; small cells are documented. | MEASURE 2.3 | SR 26-2 (data selection, under conceptual soundness) |
| G6 | **Disparities without demographic data** | The firm does not collect protected attributes, so it cannot see disparities directly. | Use legally reviewed observable proxies to look for disparities. | A reviewed proxy map exists and is tested routinely. | MEASURE 2.11 | Fair treatment |

## C: [Conflicts of interest](../03-research/conflicts-of-interest.md)

Do own-brand products get recommended more than the client's interest justifies?

| ID | Test | What goes wrong for the client | How to test | Passes if | NIST AI RMF | Regulatory hook |
|---|---|---|---|---|---|---|
| [C1 ▶](../05-illustrations/c1_proprietary_product_tilt.py) | **Proprietary product tilt** | The model favours own-brand funds over comparable cheaper options without adequate disclosure. | Compare the share of own-brand products recommended with a product-neutral benchmark, by client segment. | No unexplained tilt; any tilt is disclosed specifically enough for informed consent. | MEASURE 2.11 | Duty of loyalty (IA-5248); SEC order IA-5826 (SoFi Wealth, 2021) |

## S: [Statistical rigour](../03-research/statistical-rigour.md)

Are the reported numbers honest about variance, overfitting and multiple testing?

| ID | Test | What goes wrong for the client | How to test | Passes if | NIST AI RMF | Regulatory hook |
|---|---|---|---|---|---|---|
| [S1 ▶](../05-illustrations/s1_nested_cross_validation.py) | **Nested cross-validation** | Features or thresholds chosen on the whole dataset make the cross-validated score look better than reality. | Re-run every data-driven choice inside the cross-validation folds and compare with the reported score. | The reported performance is the nested number, or the gap is documented. | MEASURE 2.5 | SR 26-2 (outcomes analysis) |
| [S2 ▶](../05-illustrations/f3_worst_group_intersectional.py) | **Multiple testing across the suite** | Running hundreds of test slices produces failures by chance alone, and real ones get lost. | Collect every slice's p-value and control the false discovery rate (Benjamini-Hochberg). | Every pass/fail statement is backed by the corrected table. | MEASURE 2.13 | SR 26-2 (effective challenge) |
| [S3 ▶](../05-illustrations/s3_selection_stability.py) | **Feature-selection stability** | The "top drivers" the firm discloses would change with slightly different data. | Bootstrap the feature-importance or selection step and measure how often each feature is chosen. | Every disclosed driver is selected in at least the agreed share of resamples. | MEASURE 2.9 | Disclosure of how the algorithm works |
| S4 | **Bias-variance decomposition** | A headline error rate hides whether the problem is a wrong model, an unstable one, or noise. | Refit on bootstrap resamples and split error into bias, variance and noise per risk bucket. | The dominant error source is identified for every bucket that misses its target. | MEASURE 2.5 | SR 26-2 (outcomes analysis) |
| S5 | **Effective complexity against data** | The system has more effective parameters than its data can support, so validation numbers are optimistic. | Estimate effective degrees of freedom per component and compare with the size of the validation data. | The ratio is within the agreed limit, or a written justification exists. | MEASURE 2.5 | SR 26-2 (conceptual soundness) |

## R: [Reliability when the world shifts](../03-research/shift-and-dependence.md)

Which changes in clients, markets or the model itself would break the model, and would anyone notice?

| ID | Test | What goes wrong for the client | How to test | Passes if | NIST AI RMF | Regulatory hook |
|---|---|---|---|---|---|---|
| [R1 ▶](../05-illustrations/p5_intervals_on_risk_metrics.py) | **Dependent data** | Clients or days are not independent, so confidence intervals and p-values are too narrow. | Use clustered or block resampling and time-ordered validation. (Also used in P2 and P5: moving-block bootstrap of daily returns.) | All reported intervals respect the dependence in the data. | MEASURE 2.5 | SR 26-2 |
| R2 | **Writing down which shifts matter** | The team cannot say which changes in the world would break the model. | Draw the causal diagram of the model's inputs and mark which relationships may change between environments. | A reviewed diagram exists; outputs are stable on data spanning the identified shifts. | MAP 2.3 | SR 26-2 (conceptual soundness) |
| R3 | **Transfer to a new environment** | A model validated on one market or channel performs worse in another. | Evaluate separately on each environment the model is used in. | The gap between environments is within tolerance. | MEASURE 2.3 | Duty of care |
| R4 | **Feedback loops** | The model's own recommendations reshape the data it will be retrained on. | Track recommendation and acceptance rates by group and asset class across versions. | No unexplained self-reinforcing trend. | MEASURE 3.1 | Duty of loyalty (conflicts) |
| R5 | **Wrong model shape** | The model's assumed form (linear, monotone, independent) is wrong in parts of the input space. | Compare against a flexible challenger region by region. | No region shows misspecification beyond tolerance. | MEASURE 2.5 | SR 26-2 (conceptual soundness) |

## O: [The model in operation](../03-research/operation.md)

Is the chosen model justified against alternatives, and does it depend too much on one input?

| ID | Test | What goes wrong for the client | How to test | Passes if | NIST AI RMF | Regulatory hook |
|---|---|---|---|---|---|---|
| [O1 ▶](../05-illustrations/o1_single_feature_dominance.py) | **Single-feature dominance** | One input drives most decisions, so one bad data feed breaks the model. | Neutralise each input in turn and measure how much decisions change. | No single input dominates beyond the agreed share. | MEASURE 2.5 | SR 26-2 |
| O2 | **Champion and challengers** | The chosen model was never compared with structurally different alternatives. | Train two different challengers on the same task and document why the champion wins. | A signed comparison exists and is refreshed. | MEASURE 2.13 | SR 26-2 (benchmarking, under conceptual soundness) |
| O3 | **Shadow challenger** | A newer model would serve clients better but nobody checks. | Run a retrained challenger in shadow and compare continuously. | Sustained outperformance is escalated within the agreed time. | MEASURE 2.4 | SR 26-2 (ongoing monitoring) |
