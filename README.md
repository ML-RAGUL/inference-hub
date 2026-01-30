# 🚀 InferenceHub

**Multi-Tenant LLM Platform** - AI for Every Business

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📖 What is InferenceHub?

InferenceHub is a **production-ready, multi-tenant LLM platform** that allows multiple businesses to use AI through a simple API. Think of it like **Stripe for AI** - any business can sign up, get an API key, and start using AI immediately.

### 🎯 Key Features

| Feature | Description |
|---------|-------------|
| **Multi-Tenant** | Multiple businesses use the same platform with complete data isolation |
| **API Key Auth** | Secure authentication with unique API keys per tenant |
| **Usage Tracking** | Track tokens, requests, and costs per tenant |
| **Quota Management** | Set monthly limits per plan (Free, Starter, Business) |
| **Business-Specific AI** | Different system prompts for Legal, Medical, E-commerce, Education |
| **Persistent Storage** | PostgreSQL database for reliable data storage |
| **Fully Dockerized** | One command deployment with Docker Compose |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT REQUEST                          │
│                    (Mobile App / Web App / API)                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI APPLICATION                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │   Auth      │  │   Rate      │  │   Business Logic        │ │
│  │ (API Keys)  │  │  Limiting   │  │  (Tenant Management)    │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
┌──────────────────────┐      ┌──────────────────────────────────┐
│     POSTGRESQL       │      │         GROQ API                 │
│  ┌────────────────┐  │      │    (Llama 3.1 Model)             │
│  │    Tenants     │  │      │                                  │
│  ├────────────────┤  │      │  - Fast inference                │
│  │  Usage Logs    │  │      │  - Cost effective                │
│  └────────────────┘  │      │  - Open source model             │
└──────────────────────┘      └──────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Groq API Key](https://console.groq.com) (Free)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/inference-hub.git
cd inference-hub
```

### 2. Setup Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your Groq API key
# GROQ_API_KEY=gsk_your_key_here
```

### 3. Run with Docker

```bash
docker-compose up --build
```

### 4. Access the API

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 📚 API Documentation

### Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Welcome message |
| `GET` | `/health` | Health check |
| `POST` | `/signup` | Register new tenant |
| `POST` | `/inference` | Send prompt, get AI response |
| `GET` | `/usage` | Check usage statistics |
| `GET` | `/tenants` | List all tenants (admin) |

---

### 1. Sign Up - Register a New Tenant

```bash
curl -X POST "http://localhost:8000/signup?business_name=CityMedical&email=contact@citymedical.com&business_type=medical"
```

**Response:**
```json
{
  "message": "Welcome to InferenceHub, CityMedical!",
  "tenant_id": 1,
  "api_key": "sk_live_a1b2c3d4e5f6...",
  "plan": "free",
  "monthly_quota": 1000,
  "warning": "⚠️ Save this API key! You won't see it again."
}
```

**Business Types Available:**
- `legal` - Legal assistant with IPC/law knowledge
- `medical` - Medical information assistant
- `ecommerce` - Product copywriter
- `education` - Teaching assistant
- `general` - General purpose AI

---

### 2. Inference - Get AI Response

```bash
curl -X POST "http://localhost:8000/inference?prompt=What%20are%20symptoms%20of%20diabetes" \
  -H "X-API-Key: sk_live_your_api_key_here"
```

**Response:**
```json
{
  "response": "Diabetes can cause symptoms including increased thirst...",
  "tenant": "CityMedical",
  "business_type": "medical",
  "tokens_used": 450,
  "response_time_ms": 892,
  "requests_remaining": 999,
  "model": "llama-3.1-8b-instant"
}
```

---

### 3. Check Usage

```bash
curl -X GET "http://localhost:8000/usage" \
  -H "X-API-Key: sk_live_your_api_key_here"
```

**Response:**
```json
{
  "tenant": "CityMedical",
  "plan": "free",
  "usage": {
    "total_quota": 1000,
    "used": 5,
    "remaining": 995,
    "usage_percentage": 0.5
  },
  "billing_period": "monthly"
}
```

---

## 🔧 Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | High-performance async API framework |
| **PostgreSQL** | Relational database for persistent storage |
| **SQLAlchemy** | ORM for database operations |
| **Groq API** | Fast LLM inference (Llama 3.1) |
| **Docker** | Containerization for consistent deployments |
| **Docker Compose** | Multi-container orchestration |

---

## 📁 Project Structure

```
inference-hub/
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   └── db/
│       ├── __init__.py
│       ├── database.py      # Database connection
│       └── models.py        # SQLAlchemy models
├── docker/
├── tests/
├── docs/
├── .env.example             # Environment template
├── .gitignore               # Git ignore rules
├── .dockerignore            # Docker ignore rules
├── Dockerfile               # App container definition
├── docker-compose.yml       # Multi-container setup
├── requirements.txt         # Python dependencies
├── init_db.py               # Database initialization
└── README.md                # This file
```

---

## 🗄️ Database Schema

### Tenants Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| business_name | String | Company name |
| email | String | Unique email |
| api_key | String | Unique API key |
| business_type | String | legal/medical/ecommerce/education/general |
| plan | String | free/starter/business/enterprise |
| monthly_quota | Integer | Request limit per month |
| requests_used | Integer | Requests consumed |
| created_at | DateTime | Registration timestamp |

### Usage Logs Table

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| tenant_id | Integer | Foreign key to tenants |
| prompt | Text | User's prompt (truncated) |
| tokens_used | Integer | Tokens consumed |
| model | String | Model used |
| cost | Float | Cost in currency |
| response_time_ms | Integer | Response latency |
| created_at | DateTime | Request timestamp |

---

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# Rebuild and start
docker-compose up --build

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f app
```

---

## 🔐 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GROQ_API_KEY` | Your Groq API key | `gsk_xxxx...` |
| `DATABASE_URL` | PostgreSQL connection | `postgresql://user:pass@db:5432/dbname` |
| `DEBUG` | Debug mode | `true` / `false` |

---

## 📊 Pricing Plans

| Plan | Requests/Month | Rate Limit | Price |
|------|----------------|------------|-------|
| **Free** | 1,000 | 10/min | ₹0 |
| **Starter** | 50,000 | 60/min | ₹999 |
| **Business** | 500,000 | 200/min | ₹4,999 |
| **Enterprise** | Unlimited | 1000/min | Custom |

---

## 🧪 Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/ -v
```

---

## 🚀 Deployment

### Deploy to AWS ECS

1. Push Docker image to ECR
2. Create ECS cluster
3. Set up RDS PostgreSQL
4. Configure environment variables
5. Deploy service

### Deploy to Railway (Easy)

1. Connect GitHub repo
2. Add environment variables
3. Deploy automatically

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Ragul**

- Building AI Infrastructure for the future
- Open to opportunities in Backend/DevOps/AI Engineering

---

## ⭐ Star History

If this project helped you, please give it a ⭐!

---

## 🔮 Roadmap

- [ ] Rate limiting with Redis
- [ ] Load testing (50,000+ requests)
- [ ] Admin dashboard
- [ ] Webhook notifications
- [ ] Custom model fine-tuning
- [ ] Multi-region deployment
