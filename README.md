# Corporate FX Exposure & Cross-Border Hedging

Python and Excel case study comparing the EUR cost of a future USD payment under four treasury strategies: unhedged exposure, full forward hedge, FX option protection and partial forward hedging.

## Business case

A euro-area company must pay **USD 100,000 in three months**. Because EUR/USD is quoted as USD per EUR, a fall in EUR/USD means that each euro buys fewer dollars and the payable becomes more expensive in EUR.

The project answers three practical treasury questions:

1. What is the unhedged EUR cost under different terminal exchange rates?
2. What EUR budget can be locked with a forward derived from covered interest parity?
3. How do an option premium and a partial hedge change protection and upside participation?

All inputs are illustrative and are not live market quotations.

## Model

The theoretical forward is calculated as:

`F = S × (1 + r_USD × T) / (1 + r_EUR × T)`

The scenario engine then compares:

- **Unhedged:** USD notional divided by terminal EUR/USD;
- **Forward:** USD notional divided by the fixed forward rate;
- **Option:** the lower of market conversion cost and protected strike cost, plus premium;
- **Partial forward:** weighted combination of the forward and unhedged costs.

The comparison is based on payment cost and budget certainty. The lowest-cost strategy in one scenario is not automatically the best risk-management decision.

## Illustrative inputs

| Input | Value |
|---|---:|
| USD payable | 100,000 |
| Spot EUR/USD | 1.1600 |
| EUR annual rate | 2.00% |
| USD annual rate | 4.00% |
| Maturity | 0.25 year |
| Option strike | 1.1600 |
| Indicative option premium | 1.50% of initial EUR equivalent |
| Partial hedge ratio | 50% |

With these assumptions, the theoretical three-month forward is approximately **1.1658 USD per EUR**, fixing an indicative budget of approximately **EUR 85,780**.

## Repository structure

```text
src/fx_hedging.py        Scenario and export engine
tests/test_fx_hedging.py Financial logic and validation tests
requirements.txt         Python dependencies
outputs/                 Generated CSV and chart (created at runtime)
```

The original Excel workbook remains available as an auditable companion model.

## Run the project

```bash
python -m venv .venv
python -m pip install -r requirements.txt
python -m src.fx_hedging
pytest -q
```

The program generates `outputs/fx_hedging_scenarios.csv` and `outputs/fx_hedging_costs.png`.

## Skills demonstrated

- FX exposure analysis and EUR/USD quotation conventions;
- forward pricing through covered interest parity;
- comparison of forwards, options and hedge ratios;
- scenario analysis, treasury budgeting and risk interpretation;
- reproducible Python modelling, data export and automated testing.

## Limitations and extensions

The option premium is an illustrative input rather than a market-calibrated Garman-Kohlhagen price. Potential extensions include volatility-based option pricing, hedge-effectiveness metrics, rolling historical scenarios and sensitivity analysis across hedge ratios.

## Author

Sofia Kammoune — MBA Trading & Finance de Marché, ESLSCA Business School Paris.

Educational portfolio project; not investment advice.
