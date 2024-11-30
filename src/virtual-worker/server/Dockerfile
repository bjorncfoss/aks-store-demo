# server/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .
COPY order_service_pb2.py .
COPY order_service_pb2_grpc.py .

EXPOSE 50052

CMD ["python", "server.py"]