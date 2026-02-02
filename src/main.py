from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException, Header, Depends
from contextlib import asynccontextmanager
from datetime import datetime
import secrets
import time
from groq import Groq
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import os

# Load environment variables
load_dotenv()

# Import database stuff
from src.db.database import get_db, engine, Base
from src.db.models import Tenant, UsageLog


# ============================
# STARTUP EVENT
# ============================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Runs on startup and shutdown"""
    # Startup: Create tables
    print("🚀 Starting InferenceHub...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables ready!")
    yield
    # Shutdown
    print("👋 Shutting down InferenceHub...")


app = FastAPI(
    title="InferenceHub",
    description="Multi-Tenant LLM Platform",
    version="1.0.0",
    lifespan=lifespan
)
# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve UI at root
@app.get("/", response_class=FileResponse)
async def serve_ui():
    return FileResponse("static/index.html")

# ============================
# CONFIGURATION
# ============================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found! Add it to .env file")

groq_client = Groq(api_key=GROQ_API_KEY)

# System prompts for different business types
SYSTEM_PROMPTS = {
    "legal": """You are a legal assistant for an Indian law firm.
Always cite relevant sections and acts when applicable.
Add disclaimer: "This is for educational purposes only, not legal advice."
Be precise and use formal legal language.""",

    "medical": """You are a helpful medical information assistant.
Use simple language patients can understand.
Always recommend consulting a doctor for serious concerns.
Add disclaimer: "This is for educational purposes only, not medical advice."
Never diagnose or prescribe medications.""",

    "ecommerce": """You are a product copywriter and customer service assistant.
Write compelling, honest product descriptions.
Be helpful and friendly with customer queries.
Focus on benefits, not just features.""",

    "education": """You are a friendly teacher who explains concepts clearly.
Use simple language and examples.
Break down complex topics into easy steps.
Encourage questions and learning.""",

    "general": """You are a helpful AI assistant.
Be clear, accurate, and helpful.
If you don't know something, say so."""
}


# ============================
# HELPER FUNCTIONS
# ============================

def get_tenant_by_api_key(db: Session, api_key: str) -> Tenant:
    """Find tenant by API key"""
    return db.query(Tenant).filter(Tenant.api_key == api_key).first()


# ============================
# ENDPOINTS
# ============================

@app.get("/")
def home():
    return {
        "name": "InferenceHub",
        "message": "Multi-Tenant LLM Platform",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "database": "connected"
    }


@app.post("/signup")
def signup(
    business_name: str, 
    email: str, 
    business_type: str = "general",
    db: Session = Depends(get_db)
):
    """
    Register a new tenant and get API key
    
    business_type options: legal, medical, ecommerce, education, general
    """
    
    # Check if email already exists
    existing = db.query(Tenant).filter(Tenant.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Generate unique API key
    api_key = "sk_live_" + secrets.token_hex(16)
    
    # Create tenant in database
    tenant = Tenant(
        business_name=business_name,
        email=email,
        api_key=api_key,
        business_type=business_type,
        plan="free",
        monthly_quota=1000,
        requests_used=0
    )
    
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    
    return {
        "message": f"Welcome to InferenceHub, {business_name}!",
        "tenant_id": tenant.id,
        "api_key": api_key,
        "plan": "free",
        "monthly_quota": 1000,
        "warning": "⚠️ Save this API key! You won't see it again."
    }


@app.post("/inference")
def inference(
    prompt: str,
    x_api_key: str = Header(alias="X-API-Key"),
    db: Session = Depends(get_db)
):
    """
    Send a prompt and get AI response
    
    Requires X-API-Key header with your API key
    """
    
    # Start timer
    start_time = time.time()
    
    # 1. Check if API key exists
    tenant = get_tenant_by_api_key(db, x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # 2. Check quota
    remaining = tenant.monthly_quota - tenant.requests_used
    if remaining <= 0:
        raise HTTPException(status_code=429, detail="Quota exceeded. Please upgrade your plan.")
    
    # 3. Get system prompt based on business type
    system_prompt = SYSTEM_PROMPTS.get(tenant.business_type, SYSTEM_PROMPTS["general"])
    
    # 4. Call Groq API
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024
        )
        ai_response = response.choices[0].message.content
        tokens_used = response.usage.total_tokens
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")
    
    # 5. Calculate response time
    response_time_ms = int((time.time() - start_time) * 1000)
    
    # 6. Update tenant usage
    tenant.requests_used += 1
    
    # 7. Log the usage
    usage_log = UsageLog(
        tenant_id=tenant.id,
        prompt=prompt[:500],  # Store first 500 chars only
        tokens_used=tokens_used,
        model="llama-3.1-8b-instant",
        cost=tokens_used * 0.0001,  # Example cost calculation
        response_time_ms=response_time_ms
    )
    db.add(usage_log)
    db.commit()
    
    # 8. Return response
    return {
        "response": ai_response,
        "tenant": tenant.business_name,
        "business_type": tenant.business_type,
        "tokens_used": tokens_used,
        "response_time_ms": response_time_ms,
        "requests_remaining": tenant.monthly_quota - tenant.requests_used,
        "model": "llama-3.1-8b-instant"
    }


@app.get("/usage")
def get_usage(
    x_api_key: str = Header(alias="X-API-Key"),
    db: Session = Depends(get_db)
):
    """
    Check your usage and remaining quota
    """
    
    tenant = get_tenant_by_api_key(db, x_api_key)
    if not tenant:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    # Get usage stats
    remaining = tenant.monthly_quota - tenant.requests_used
    usage_percentage = round((tenant.requests_used / tenant.monthly_quota) * 100, 2)
    
    return {
        "tenant": tenant.business_name,
        "plan": tenant.plan,
        "usage": {
            "total_quota": tenant.monthly_quota,
            "used": tenant.requests_used,
            "remaining": remaining,
            "usage_percentage": usage_percentage
        },
        "billing_period": "monthly",
        "member_since": tenant.created_at.isoformat() if tenant.created_at else None
    }


@app.get("/tenants")
def list_tenants(db: Session = Depends(get_db)):
    """
    List all tenants (Admin endpoint - for testing)
    """
    tenants = db.query(Tenant).all()
    return {
        "total": len(tenants),
        "tenants": [
            {
                "id": t.id,
                "business_name": t.business_name,
                "email": t.email,
                "business_type": t.business_type,
                "plan": t.plan,
                "requests_used": t.requests_used
            }
            for t in tenants
        ]
    }
