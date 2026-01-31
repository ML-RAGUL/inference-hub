"""
InferenceHub Load Testing
=========================
Run: locust -f locustfile.py --host=http://localhost:8000

This simulates multiple tenants using the platform simultaneously.
"""

from locust import HttpUser, task, between
import random
import string


class TenantUser(HttpUser):
    """Simulates a tenant using InferenceHub"""
    
    # Wait 1-3 seconds between requests (realistic user behavior)
    wait_time = between(1, 3)
    
    api_key = None
    tenant_name = None
    
    def on_start(self):
        """Called when a simulated user starts - creates a new tenant"""
        
        # Generate random tenant details
        random_id = ''.join(random.choices(string.ascii_lowercase, k=6))
        self.tenant_name = f"loadtest_{random_id}"
        email = f"{random_id}@loadtest.com"
        
        # Signup and get API key
        business_types = ["legal", "medical", "ecommerce", "education", "general"]
        
        response = self.client.post(
            "/signup",
            params={
                "business_name": self.tenant_name,
                "email": email,
                "business_type": random.choice(business_types)
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            self.api_key = data["api_key"]
        else:
            # If signup fails (duplicate email), try again with different email
            pass
    
    @task(10)
    def inference_request(self):
        """Main task - send inference requests (10x weight)"""
        
        if not self.api_key:
            return
        
        prompts = [
            "What are the symptoms of diabetes?",
            "Explain Section 420 of IPC",
            "Write a product description for headphones",
            "How does photosynthesis work?",
            "What is machine learning?",
            "Explain the water cycle",
            "What are the benefits of exercise?",
            "How to write a good resume?",
            "What is cloud computing?",
            "Explain REST API"
        ]
        
        self.client.post(
            "/inference",
            params={"prompt": random.choice(prompts)},
            headers={"X-API-Key": self.api_key}
        )
    
    @task(3)
    def check_usage(self):
        """Check usage stats (3x weight)"""
        
        if not self.api_key:
            return
        
        self.client.get(
            "/usage",
            headers={"X-API-Key": self.api_key}
        )
    
    @task(1)
    def health_check(self):
        """Health check endpoint (1x weight)"""
        
        self.client.get("/health")


class QuickUser(HttpUser):
    """Fast user - only hits lightweight endpoints"""
    
    wait_time = between(0.5, 1)
    
    @task
    def health_check(self):
        """Just health checks - for testing max throughput"""
        self.client.get("/health")
