"""
Test Groq API Connection
========================
Run this to verify your Groq API key works.

Usage:
    python test_groq.py
"""

from groq import Groq
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("❌ GROQ_API_KEY not found!")
    print("Add it to your .env file:")
    print("  GROQ_API_KEY=gsk_your_key_here")
    exit(1)

# Initialize client
client = Groq(api_key=GROQ_API_KEY)

# Test request
response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": "Say hello in Tamil"}
    ]
)

print("✅ Groq API is working!")
print("")
print("Response:")
print(response.choices[0].message.content)
