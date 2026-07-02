# ============================================
# Dockerfile for PySpark Retail Analytics App
# ============================================

# 1. Base image: official Python image
FROM python:3.10-slim

# 2. Install Java (Spark needs Java to run)
RUN apt-get update && apt-get install -y default-jre && rm -rf /var/lib/apt/lists/*

# 3. Install PySpark
RUN pip install --no-cache-dir pyspark==3.5.0

# 4. Set working directory inside the container
WORKDIR /app

# 5. Copy project files into the container
COPY app.py .
COPY synthetic_transactions.csv .

# 6. Command that runs when container starts
CMD ["python", "app.py"]
