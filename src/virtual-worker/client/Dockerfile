# client/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY client.py .
COPY order_service_pb2.py .
COPY order_service_pb2_grpc.py .

CMD ["python", "client.py"]