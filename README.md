# Exchange Destination Analyzer

An interactive, data-driven decision-support tool for comparing and ranking international exchange destinations using academic, employer, cost of living, safety and city-level indicators.

## Overview

The **Exchange Destination Analyzer** was developed to support a real international exchange decision through a structured and transparent multi-criteria framework.

The full exchange network includes a significantly larger number of partner universities. This project focuses on an initial curated sample of **28 destinations**, selected from that broader universe based on academic reputation, perceived quality, geographic preferences and personal interest.

The objective is to move from this initial shortlist to a more structured and data-driven final decision.

The tool combines external datasets with customizable user preferences, allowing users to assign different weights to each decision criterion and generate a personalized ranking of exchange destinations.

## Live Demo

A public interactive version of the application will be available through Streamlit Community Cloud.

**Live Demo:** *link to be added after deployment*

## Key Features

* Interactive ranking of 28 exchange destinations
* Customizable user-defined weights
* Dynamic multi-criteria scoring model
* University-level and city-level indicators
* Destination comparison across five dimensions
* Interactive radar chart
* Raw data explorer with country filters
* Transparent methodology and documented data sources
* Relative scoring system normalized to a common 0–100 scale

## Decision Criteria

The model evaluates each destination across five dimensions:

| Criterion               | Description                                                                         |
| ----------------------- | ----------------------------------------------------------------------------------- |
| **Academic Quality**    | Academic strength of the institution based on international subject rankings        |
| **Employer Reputation** | Employer perception of the university based on QS data                              |
| **Cost of Living**      | Relative affordability of the destination, including rent                           |
| **Safety**              | Comparative safety of the destination                                               |
| **City Attractiveness** | Overall attractiveness of the destination from an international student perspective |

## Data Sources

The model primarily relies on external and independently sourced data.

### Academic Quality

**QS World University Rankings by Subject – Business & Management Studies 2025**

The original ranking position is used as the academic input. Lower ranking positions represent stronger academic performance.

### Employer Reputation

**QS Employer Reputation – Business & Management Studies 2025**

The original QS Employer Reputation score is used as a measure of how institutions are perceived by employers.

### Cost of Living

**Numbeo Cost of Living Plus Rent Index 2025**

The Cost of Living Plus Rent Index was selected because accommodation represents a material component of expenditure for an international exchange student.

Where direct 2025 city observations were unavailable, documented proxy estimates were used.

### Safety

**Numbeo Safety Index by City 2025**

Higher values represent safer destinations.

### City Attractiveness

**QS Best Student Cities 2025**

The indicator is used to capture the relative attractiveness of each destination from an international student perspective.

## Methodology

Because the underlying variables are measured on different scales, all criteria are transformed to a common **0–100 scale** using min-max normalization.

For criteria where higher values are better:

`Score = (x - min) / (max - min) × 100`

For criteria where lower values are better, such as Academic Ranking and Cost of Living:

`Score = (max - x) / (max - min) × 100`

A score of **100** therefore represents the best-performing destination within the 28-destination sample for that specific criterion, rather than an absolute theoretical maximum.

## Weighted Ranking

Users can assign a custom weight to each criterion.

The final score is calculated as:

`Final Score = Σ (Normalized Criterion Score × User Weight)`

The five selected weights must sum to **100%**.

The resulting composite score is then used to rank destinations from highest to lowest according to the user's priorities.

The model should therefore be interpreted as a **decision-support tool rather than a universal ranking**. Results depend on both the underlying dataset and the preferences selected by the user.

## Missing Data & Proxy Treatment

Where a direct city-level observation was unavailable, a documented proxy was used rather than excluding the destination.

Examples include:

* **Ithaca:** Pittsburgh benchmark adjusted by 5%
* **Ann Arbor:** average of Pittsburgh and Columbus
* **St. Gallen:** average of Bern and Basel adjusted by 5%
* **Lille:** Lyon benchmark adjusted by 5%
* **Vallendar:** Cologne benchmark adjusted by 10%
* **Vallendar Safety:** nearby Koblenz used as reference

These assumptions are explicitly documented to keep the model transparent and reproducible.

## Application Structure

The application is organized into five sections:

### Overview

Introduces the decision problem, the destination sample and the analytical framework.

### Build Your Ranking

Allows users to customize the importance of each criterion and dynamically generate a personalized ranking.

### Compare Destinations

Allows up to three universities to be compared using an interactive radar chart and normalized factor scores.

### Explore Data

Provides access to the underlying raw dataset used by the model.

### Methodology

Documents data sources, assumptions, normalization and scoring logic.

## Technology Stack

* **Python** – application logic and scoring model
* **Pandas** – data processing and transformation
* **Streamlit** – interactive web application
* **Plotly** – interactive visualizations
* **Git / GitHub** – version control and project documentation

## Project Structure

```text
exchange-destination-analyzer/
│
├── app.py
├── destinations.csv
├── requirements.txt
├── README.md
└── .gitignore
```

## Objective

This project demonstrates how external data, quantitative analysis and user-defined preferences can be combined to improve a real-world decision involving multiple competing factors.

Although developed around international exchange selection, the underlying framework can be extended to a broad range of multi-criteria decision-making problems.

## Author

**Christian Moresco**

Finance student interested in data-driven decision making, strategy and technology.
