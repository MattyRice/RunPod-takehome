FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies and clean up in the same layer
RUN apt-get update && apt-get install -y \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies and clean cache in the same layer
RUN pip install --no-cache-dir -r requirements.txt

# Copy the handler script
COPY . .

# Use ARG for build-time variables
ARG HF_TOKEN
ENV HF_TOKEN=${HF_TOKEN}

# Set the entrypoint
CMD ["python", "handler.py"] 