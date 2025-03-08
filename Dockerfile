FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

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
RUN pip install -r requirements.txt && \
    pip cache purge

# Set Hugging Face token as environment variable
# Replace YOUR_HF_TOKEN with your actual token
ENV HF_TOKEN="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"

# Copy the handler script
COPY handler.py .

# Set the entrypoint
CMD ["python", "handler.py"] 