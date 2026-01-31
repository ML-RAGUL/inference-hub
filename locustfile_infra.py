"""
InferenceHub Load Testing - Infrastructure Only
================================================
Tests YOUR code performance, not Groq API.

Run: locust -f locustfile_infra.py --host=http://localhost:8000
"""

from locust import HttpUser, task, between
import random
import string


class InfrastructureUser(HttpUser):
    """Tests platform infrastructure without hitting Groq API"""
    
    wait_time = between(0.1, 0.5)  # Fast requests
    
    api_key = None
    
    def on_start(self):
        """Create tenant on start"""
        random_id = ''.join(random.choices(string.ascii_lowercase, k=8))
        
        response = self.client.post(
            "/signup",
            params={
                "business_name": f"loadtest_{random_id}",
                "email": f"{random_id}@test.com",
                "business_type": "general"
            }
        )
        
        if response.status_code == 200:
            self.api_key = response.json()["api_key"]
    
    @task(5)
    def health_check(self):
        """Health endpoint - tests basic server"""
        self.client.get("/health")
    
    @task(3)
    def check_usage(self):
        """Usage endpoint - tests database reads"""
        if self.api_key:
            self.client.get(
                "/usage",
                headers={"X-API-Key": self.api_key}
            )
    
    @task(2)
    def list_tenants(self):
        """List tenants - tests database query"""
        self.client.get("/tenants")
    
    @task(1)
    def signup_new_tenant(self):
        """Signup - tests database writes"""
        random_id = ''.join(random.choices(string.ascii_lowercase, k=8))
        self.client.post(
            "/signup",
            params={
                "business_name": f"load_{random_id}",
                "email": f"{random_id}@load.com",
                "business_type": random.choice(["legal", "medical", "general"])
            }
        )


class HighLoadUser(HttpUser):
    """Maximum throughput test"""
    
    wait_time = between(0.05, 0.1)  # Very fast
    
    @task
    def health_spam(self):
        """Hit health endpoint as fast as possible"""
        self.client.get("/health")
