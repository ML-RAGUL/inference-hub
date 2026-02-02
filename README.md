# InferenceHub

A multi-tenant LLM platform that enables businesses to integrate AI capabilities through a REST API. Built with FastAPI, PostgreSQL, and Llama 3.1.

## Live Demo

| Resource | URL |
|----------|-----|
| Application | http://3.26.205.39:8000 |
| API Docs | http://3.26.205.39:8000/docs |

Deployed on AWS EC2 with RDS PostgreSQL, CI/CD via GitHub Actions.

## Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│              │     │              │     │              │     │              │
│    Client    │────▶│   FastAPI    │────▶│  PostgreSQL  │     │   Groq API   │
│   Browser    │     │   (Docker)   │────▶│    (RDS)     │     │  (Llama 3.1) │
│              │◀────│              │◀────│              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                            │                                         ▲
                            │                                         │
                            └─────────────────────────────────────────┘
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI, Python 3.11 |
| Database | PostgreSQL 15 (AWS RDS) |
| ORM | SQLAlchemy |
| LLM | Groq API (Llama 3.1 8B) |
| Container | Docker |
| Cloud | AWS EC2, RDS, CloudWatch |
| CI/CD | GitHub Actions |

## Features

**Multi-Tenancy** - Each business gets isolated data, unique API key, and usage tracking.

**Business-Specific AI** - System prompts adapt based on business type:
- Medical: Patient-friendly explanations with disclaimers
- Legal: Formal language with IPC references
- E-Commerce: Product descriptions, customer service
- Education: Teaching-focused explanations
- General: Default assistant behavior

**Usage Tracking** - Every request logged with tokens used, cost, and response time.

**Quota Management** - Monthly limits per tenant with automatic enforcement.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /signup | Register tenant, get API key |
| POST | /inference | Send prompt, get AI response |
| GET | /usage | Check quota and usage stats |
| GET | /docs | Swagger documentation |

## Quick Start

**Prerequisites:** Docker, Groq API key

```bash
git clone https://github.com/ML-RAGUL/inference-hub.git
cd inference-hub

cp .env.example .env
# Add your GROQ_API_KEY to .env

docker-compose up --build
```

Open http://localhost:8000

## Project Structure

```
inference-hub/
├── src/
│   ├── main.py              # FastAPI app, routes
│   └── db/
│       ├── database.py      # DB connection
│       └── models.py        # SQLAlchemy models
├── static/
│   └── index.html           # Frontend UI
├── .github/
│   └── workflows/
│       └── deploy.yml       # CI/CD pipeline
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Database Schema

**tenants**
- id, business_name, email, api_key, business_type
- plan, monthly_quota, requests_used, created_at

**usage_logs**
- id, tenant_id, prompt, tokens_used, model
- cost, response_time_ms, created_at

## AWS Deployment

```
┌─────────────────────────────────────────────────────────────┐
│                    AWS Cloud (Sydney)                       │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │    EC2      │    │    RDS      │    │ CloudWatch  │     │
│  │  (Docker)   │───▶│ (PostgreSQL)│    │ (Monitoring)│     │
│  │  t3.micro   │    │ db.t4g.micro│    │   Alarms    │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Components:**
- EC2 (t3.micro) - Runs Docker container with FastAPI
- RDS (db.t4g.micro) - Managed PostgreSQL with auto-backups
- CloudWatch - CPU monitoring with email alerts
- Security Groups - Firewall rules for ports 22, 8000, 5432

## CI/CD Pipeline

On every push to main:

1. **Test Job** - Checkout code, install dependencies, syntax check
2. **Deploy Job** - SSH to EC2, pull code, rebuild Docker container

```yaml
# .github/workflows/deploy.yml
- git pull origin main
- sudo docker-compose down
- sudo docker-compose up --build -d
```

## Load Test Results

Tested with Locust under 100 concurrent users:

| Metric | Result |
|--------|--------|
| Requests/sec (sustained) | 200+ |
| Requests/sec (peak) | 580 |
| Failure rate | 0% |
| Median response time | 200-300ms |
| 95th percentile | 600-850ms |

Bottleneck is external LLM API rate limits, not application code.

## Environment Variables

| Variable | Description |
|----------|-------------|
| GROQ_API_KEY | API key from console.groq.com |
| DATABASE_URL | PostgreSQL connection string |

## What I Learned

- Multi-tenant architecture with API key isolation
- FastAPI async request handling
- SQLAlchemy ORM with PostgreSQL
- Docker containerization and compose
- AWS EC2, RDS, CloudWatch setup
- CI/CD with GitHub Actions
- SSH key management and security groups
- Load testing with Locust

## Future Improvements

- Redis caching for repeated queries
- Rate limiting per tenant
- HTTPS with custom domain
- Kubernetes for auto-scaling
- Unit tests with pytest

## License

MIT
