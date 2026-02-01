# InferenceHub

A multi-tenant LLM platform that enables businesses to integrate AI capabilities through a simple REST API. Built with FastAPI, PostgreSQL, and Llama 3.1.

## Live Demo

| Resource | URL |
|----------|-----|
| API | http://3.26.181.226:8000 |
| Swagger Docs | http://3.26.181.226:8000/docs |

Deployed on AWS EC2 (ap-southeast-2) with Docker.

## Why This Project?

Most businesses want to use LLMs but face common challenges:
- Setting up and maintaining AI infrastructure is complex
- Managing multiple clients with isolated data is difficult
- Tracking usage and costs per client requires custom solutions

InferenceHub solves these by providing a ready-to-deploy platform where each tenant gets:
- Unique API key for authentication
- Isolated data and usage tracking
- Business-specific AI behavior (legal, medical, e-commerce, etc.)
- Monthly quota management

## Architecture

```
Client Request
      |
      v
+------------------+
|    FastAPI       |
|  (Auth + Routes) |
+--------+---------+
         |
    +----+----+
    |         |
    v         v
+-------+  +--------+
|  DB   |  |  Groq  |
| (PG)  |  | (LLM)  |
+-------+  +--------+
```

**Tech Stack:**
- FastAPI - Async API framework
- PostgreSQL - Persistent storage
- SQLAlchemy - ORM
- Groq API - LLM inference (Llama 3.1 8B)
- Docker - Containerization
- AWS EC2 - Cloud deployment

## Load Test Results

Tested with Locust under 100 concurrent users:

| Metric | Result |
|--------|--------|
| Requests/sec (sustained) | 200+ |
| Requests/sec (peak) | 580 |
| Failure rate | 0% |
| Median response time | 200-300ms |
| 95th percentile | 600-850ms |

Infrastructure handles high load. External LLM API is the bottleneck, not the application code.

## Quick Start

**Prerequisites:** Docker, Groq API key (free at console.groq.com)

```bash
# Clone
git clone https://github.com/ML-RAGUL/inference-hub.git
cd inference-hub

# Configure
cp .env.example .env
# Add your GROQ_API_KEY to .env

# Run
docker-compose up --build
```

API available at `http://localhost:8000/docs`

## API Endpoints

### Register Tenant
```bash
POST /signup?business_name=MyCompany&email=test@example.com&business_type=medical
```
Returns API key for authentication.

### Get AI Response
```bash
POST /inference?prompt=What are symptoms of diabetes
Header: X-API-Key: sk_live_xxx
```
Response includes AI output, tokens used, and remaining quota.

### Check Usage
```bash
GET /usage
Header: X-API-Key: sk_live_xxx
```
Returns quota consumption and billing info.

## Business Types

Each type has a specialized system prompt:

| Type | Use Case |
|------|----------|
| legal | Law firms - IPC sections, legal terminology |
| medical | Healthcare - Patient-friendly explanations |
| ecommerce | Retail - Product descriptions, customer service |
| education | EdTech - Teaching explanations |
| general | Default - General purpose assistant |

## Project Structure

```
inference-hub/
├── src/
│   ├── main.py           # API endpoints
│   └── db/
│       ├── database.py   # DB connection
│       └── models.py     # SQLAlchemy models
├── locustfile.py         # Load tests (with AI)
├── locustfile_infra.py   # Load tests (infrastructure)
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Database Schema

**tenants** - Stores registered businesses
- id, business_name, email, api_key, business_type, plan, monthly_quota, requests_used

**usage_logs** - Tracks every API request
- id, tenant_id, prompt, tokens_used, model, cost, response_time_ms

## Local Development

Without Docker:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start PostgreSQL separately, then:
python init_db.py
uvicorn src.main:app --reload
```

## Load Testing

```bash
# Install
pip install locust

# Test infrastructure (without AI calls)
locust -f locustfile_infra.py --host=http://localhost:8000

# Test full flow (with AI calls)
locust -f locustfile.py --host=http://localhost:8000
```

Open http://localhost:8089 to run tests.

## AWS Deployment

Deployed on AWS EC2 (t3.micro) in ap-southeast-2 region.

Steps to deploy:
1. Launch EC2 instance (Ubuntu 24.04)
2. Install Docker and Docker Compose
3. Clone repository
4. Configure environment variables
5. Run `docker-compose up --build -d`
6. Open port 8000 in security group

## Configuration

Environment variables (`.env`):

| Variable | Description |
|----------|-------------|
| GROQ_API_KEY | API key from console.groq.com |
| DATABASE_URL | PostgreSQL connection string |

## What I Learned

Building this project helped me understand:
- Designing multi-tenant architectures with proper data isolation
- API authentication patterns using API keys
- Database modeling with SQLAlchemy ORM
- Containerizing Python applications with Docker
- Load testing with Locust to identify bottlenecks
- External API rate limits and how to handle them
- AWS EC2 deployment and security group configuration
- SSH key management and Linux server administration

## License

MIT
