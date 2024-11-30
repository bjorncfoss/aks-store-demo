# src/virtual-worker/client/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the proto file
COPY order_service.proto .

# Generate protobuf files
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. order_service.proto

# Copy the application code
COPY server.py .
COPY order_service_pb2.py .
COPY order_service_pb2_grpc.py .

CMD ["python", "server.py"]