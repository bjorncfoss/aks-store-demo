import grpc
import time
import random
import os
from datetime import datetime
from prometheus_client import start_http_server, Summary, Counter, Gauge
import worker_pb2
import worker_pb2_grpc

def main():
    print(f"[INFO] Virtual Customer started at {datetime.now()}")

    # Prometheus metrics
    REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
    ORDER_COUNTER = Counter('orders_total', 'Total number of orders processed')
    ORDER_SIZE_GAUGE = Gauge('order_size_items', 'Number of items in an order')
    PROMETHEUS_PORT = 8000  # Change if needed
    start_http_server(PROMETHEUS_PORT)
    print(f"[INFO] Prometheus metrics server started on port {PROMETHEUS_PORT}")

    # gRPC server address
    grpc_server_address = "localhost:50051"  # Update with the actual worker server address

    # Order configuration
    orders_per_hour = int(os.getenv("ORDERS_PER_HOUR", "100"))
    if orders_per_hour == 0:
        print("[ERROR] ORDERS_PER_HOUR cannot be zero.")
        return

    order_submission_interval = 3600 / orders_per_hour
    print(f"[INFO] Interval between orders: {order_submission_interval:.2f} seconds")

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
                    print(f"[INFO] Order {order.order_id} sent successfully in {elapsed_time:.2f}s. "
                          f"Response: {response.message}")
                else:
                    print(f"[ERROR] Order {order.order_id} failed. Response: {response.message}")
        except grpc.RpcError as e:
            print(f"[ERROR] gRPC request error: {e}")

        # Wait before sending the next order
        time.sleep(order_submission_interval)

if __name__ == "__main__":
    main()
