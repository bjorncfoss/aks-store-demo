# src/virtual-worker/client/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Generate protobuf files if necessary
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. order_service.proto

COPY client.py .
COPY order_service_pb2.py .
COPY order_service_pb2_grpc.py .

CMD ["python", "client.py"]