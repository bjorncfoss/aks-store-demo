import grpc
import time
import random
import os
import signal
import sys
from datetime import datetime
from prometheus_client import start_http_server, Summary, Counter, Gauge
import logging
import worker_pb2
import worker_pb2_grpc

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def handle_shutdown(signum, frame):
    logging.info("[INFO] Virtual Customer shutting down...")
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)

def main():
    logging.info(f"Virtual Customer started at {datetime.now()}")

    # Prometheus metrics
    REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
    ORDER_COUNTER = Counter('orders_total', 'Total number of orders processed')
    ORDER_SIZE_GAUGE = Gauge('order_size_items', 'Number of items in an order')
    PROMETHEUS_PORT = int(os.getenv("PROMETHEUS_PORT", "8000"))
    start_http_server(PROMETHEUS_PORT)
    logging.info(f"Prometheus metrics server started on port {PROMETHEUS_PORT}")

    # gRPC server address
    grpc_server_address = os.getenv("ORDER_SERVICE_URL", "order-service:50051")  # Use Kubernetes service
    logging.info(f"Connecting to gRPC server at {grpc_server_address}")

    # Order configuration
    try:
        orders_per_hour = int(os.getenv("ORDERS_PER_HOUR", "3000"))
        if orders_per_hour <= 0:
            raise ValueError("ORDERS_PER_HOUR must be greater than zero.")
    except ValueError as e:
        logging.error(f"Invalid ORDERS_PER_HOUR: {e}")
        return

    order_submission_interval = 3600 / orders_per_hour
    logging.info(f"Interval between orders: {order_submission_interval:.2f} seconds")

    # gRPC channel and stub
    channel = grpc.insecure_channel(grpc_server_address)
    stub = worker_pb2_grpc.WorkerServiceStub(channel)

    order_counter = 0
    start_time = datetime.now()

    while True:
        order_counter += 1

        # Generate a random order
        customer_id = str(random.randint(1, 100))
        number_of_items = random.randint(1, 5)
        items = [
            worker_pb2.Item(
                product_id=str(random.randint(1, 10)),
                quantity=random.randint(1, 5),
                price=round(random.uniform(1.0, 10.0), 2)
            )
            for _ in range(number_of_items)
        ]

        order = worker_pb2.OrderRequest(
            order_id=f"order-{order_counter}",
            customer_id=customer_id,
            items=items
        )

        ORDER_COUNTER.inc()
        ORDER_SIZE_GAUGE.set(len(items))

        try:
            with REQUEST_TIME.time():  # Track request processing time
                response = stub.ProcessOrder(order)
                elapsed_time = (datetime.now() - start_time).total_seconds()

                if response.success:
                    logging.info(f"Order {order.order_id} sent successfully in {elapsed_time:.2f}s. "
                                 f"Response: {response.message}")
                else:
                    logging.error(f"Order {order.order_id} failed. Response: {response.message}")
        except grpc.RpcError as e:
            logging.error(f"gRPC request error: {e}")

        # Wait before sending the next order
        time.sleep(order_submission_interval)

if __name__ == "__main__":
    main()
