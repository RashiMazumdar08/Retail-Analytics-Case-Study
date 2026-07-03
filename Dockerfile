# ==========================================
# Dockerfile - PySpark Retail Analytics
# ==========================================

# Base Image
FROM python:3.10-slim

# Install Java (Required for Spark)
RUN apt-get update && \
    apt-get install -y default-jre && \
    apt-get clean

# Set JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$PATH:$JAVA_HOME/bin

# Set Working Directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir \
    pyspark==3.5.0 \
    pandas \
    numpy \
    matplotlib \
    scikit-learn

# Run application
CMD ["python", "app.py"]
