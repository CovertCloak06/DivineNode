# Use slim Python (switch to CUDA base later if you have GPUs)
FROM python:3.10-slim

WORKDIR /app
RUN apt-get update && apt-get install -y build-essential git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
WORKDIR /app/src
CMD ["python", "train.py", "--epochs", "1"]
