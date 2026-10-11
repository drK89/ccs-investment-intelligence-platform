# CCS Investment Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-unittest-success)](#testing)
[![Data](https://img.shields.io/badge/data-synthetic-orange)](docs/DATA_DICTIONARY.md)
[![Licence](https://img.shields.io/badge/licence-All%20Rights%20Reserved-lightgrey)](LICENSE)

A transparent decision-support application for screening, comparing and stress-testing carbon capture and storage project scenarios.

The project demonstrates how structured data, configurable priorities and explainable analytics can support an early portfolio conversation without replacing engineering, commercial, legal, regulatory or investment due diligence.

## Portfolio highlights

- Clean Python package with reusable scoring and validation modules
- Configurable multi-criteria project ranking
- Explainable contribution breakdown for every result
- One-way sensitivity analysis
- Monte Carlo rank-stability analysis
- Interactive Streamlit dashboard
- FastAPI service with automatic OpenAPI documentation
- SQLite audit trail for reproducible runs
- CSV export, automated tests, Docker and CI workflow
- Explicit synthetic-data and responsible-use controls

## Dashboard

The dashboard lets a user:

1. Upload a compatible project dataset or use the bundled demonstration data.
2. Adjust portfolio priorities with interactive weights.
3. Compare ranked projects and recommended next actions.
4. Inspect the factors contributing to an individual result.
5. test how rankings change when priorities change.
6. Estimate rank stability across thousands of random weight scenarios.
7. Download the complete ranked result.

## Architecture

~~~text
CSV / user upload
       |
       v
data validation -----> clear validation errors
       |
       v
generic scoring engine -----> explanation breakdown
       |                         |
       +----> sensitivity -------+
       +----> Monte Carlo -------+
       +----> SQLite audit trail
       |
       +----> Streamlit dashboard
       +----> FastAPI endpoints
       +----> CSV / JSON outputs
~~~

## Repository structure

~~~text
.
├── data/
│   └── demo_projects.csv
├── docs/
│   ├── CONFIDENTIALITY_AND_SCOPE.md
│   ├── DATA_DICTIONARY.md
│   └── METHODOLOGY.md
├── outputs/
├── src/ccs_platform/
│   ├── api.py
│   ├── cli.py
│   ├── data_loader.py
│   ├── database.py
│   ├── scoring.py
│   └── sensitivity.py
├── tests/
├── dashboard.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── run_analysis.py
~~~

## Quick start

### 1. Create an environment

~~~bash
python -m venv .venv
~~~

Windows PowerShell:

~~~powershell
.venv\Scripts\Activate.ps1
~~~

macOS or Linux:

~~~bash
source .venv/bin/activate
~~~

### 2. Install dependencies

~~~bash
pip install -r requirements.txt
pip install -e .
~~~

### 3. Run the analytical pipeline

~~~bash
python run_analysis.py
~~~

Outputs are written to the `outputs` directory, including rankings, rank-stability results, a run summary and an SQLite audit database.

The repository includes example CSV and JSON outputs generated from the bundled synthetic scenarios. The local SQLite audit database is intentionally excluded from version control.

### 4. Launch the dashboard

~~~bash
streamlit run dashboard.py
~~~

### 5. Launch the API

~~~bash
uvicorn ccs_platform.api:app --reload
~~~

Open `http://127.0.0.1:8000/docs` for the interactive API documentation.

## API examples

Health check:

~~~bash
curl http://127.0.0.1:8000/health
~~~

Rank the bundled demonstration portfolio:

~~~bash
curl http://127.0.0.1:8000/rankings
~~~

Score one scenario:

~~~bash
curl -X POST http://127.0.0.1:8000/score \
  -H "Content-Type: application/json" \
  -d '{
    "values": {
      "commercial_potential": 80,
      "technology_readiness": 75,
      "environmental_benefit": 90,
      "delivery_confidence": 70,
      "infrastructure_access": 85
    }
  }'
~~~

## Methodology

The public engine uses a conventional weighted multi-criteria model. User-selected non-negative weights are normalized to 100%, and each result exposes the contribution of every criterion.

Read [Public Methodology](docs/METHODOLOGY.md) for the formula, decision bands, uncertainty analysis and limitations.

## Data statement

All bundled project names and values are **synthetic demonstration scenarios**. They are not real asset evaluations and must not be interpreted as investment recommendations. The schema is designed so a user can replace the demonstration CSV with appropriately licensed public or organisational data.

Read the [Data Dictionary](docs/DATA_DICTIONARY.md) and [Confidentiality and Scope Statement](docs/CONFIDENTIALITY_AND_SCOPE.md).

## Testing

The core platform uses the Python standard-library test runner:

~~~bash
python -m unittest discover -s tests -v
~~~

The tests cover weight normalization, score calculations, classification boundaries, data validation, sensitivity output and Monte Carlo probability consistency.

## Docker

Run the dashboard and API together:

~~~bash
docker compose up --build
~~~

- Dashboard: `http://localhost:8501`
- API documentation: `http://localhost:8000/docs`

## Responsible use

This tool supports structured early-stage discussion. It does not replace:

- subsurface characterization and storage assurance;
- capture-process and transport engineering;
- lifecycle emissions analysis;
- regulatory, permitting or legal review;
- financial modelling and independent assurance; or
- accountable human decision-making.

## Author

**Dr Khaldoun Shaker**  
Petroleum & Reservoir Engineer | Energy Data Analytics  
Edinburgh, United Kingdom  
[GitHub Portfolio](https://github.com/drK89)

## Licence

Copyright (c) 2026 Khaldoun Shaker. All rights reserved. See [LICENSE](LICENSE).

