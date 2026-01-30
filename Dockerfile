# ================================
# InferenceHub Dockerfile
# ================================
# This file tells Docker how to package our app

# Step 1: Start with Python base image
FROM python:3.11-slim

# Step 2: Set working directory inside container
WORKDIR /app

# Step 3: Copy requirements first (for caching)
COPY requirements.txt .

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy all source code
COPY . .

# Step 6: Expose port 8000
EXPOSE 8000

# Step 7: Command to run the app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
