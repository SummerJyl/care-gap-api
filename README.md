<!--
# care-gap-api

A FHIR-native care gap detection API for primary care ACOs.

## Problem
Independent primary care practices in value-based care arrangements
(like Aledade's MSSP ACOs) need to identify and close HCC coding gaps
to accurately reflect patient complexity and maximize shared savings.
Missing or undocumented HCC codes directly impact risk scores and
downstream revenue.

## What This Does
- Accepts FHIR R4 Patient Bundles via REST API
- Extracts and normalizes clinical conditions (ICD-10 codes)
- Maps conditions to CMS-HCC V28 categories
- Identifies undocumented HCC gaps based on clinical patterns
- Returns prioritized gap recommendations for care teams

## Tech Stack
- Python / FastAPI
- FHIR R4 (fhir.resources)
- PostgreSQL / SQLAlchemy
- AWS (Lambda, API Gateway, RDS)
- Docker

## Architecture
[diagram coming — Week 3]

## API Reference
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Service health check |
| POST | /api/v1/ingest | Ingest a FHIR R4 Bundle |
| GET | /api/v1/patients/{id} | Get normalized patient summary |
| GET | /api/v1/patients/{id}/gaps | Get prioritized HCC gap list |

## Running Locally
```bash
git clone https://github.com/jyliansummers/care-gap-api.git
cd care-gap-api
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Clinical Context
This project targets the CMS-HCC V28 model transition, which eliminates
over 2,000 legacy codes and requires dual-model mapping (V24 + V28)
simultaneously through 2026.

## What I'd Build Next
- SMART on FHIR authentication
- Real EHR sandbox integration (Epic, Athenahealth)
- ML-based gap prediction model
- Bulk FHIR export support ($export operation)

-->
