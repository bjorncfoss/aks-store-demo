# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy protobuf generated files and server code
COPY fetch_pb2.py fetch_pb2_grpc.py server.py ./

EXPOSE 50051

CMD ["python", "server.py"]