import grpc
import order_service_pb2
import order_service_pb2_grpc
import time
from datetime import datetime

def fetch_orders(stub):
    request = order_service_pb2.FetchOrdersRequest()
    response = stub.FetchOrders(request)
    return response.orders

def main():
    order_service_url = "localhost:50052"  # Update with your gRPC server address
    orders_per_hour = 3600  # Update with your desired orders per hour

    if orders_per_hour == 0:
        print("Please set the ORDERS_PER_HOUR environment variable")
        return

    sleep_duration = 3600 / orders_per_hour
    print(f"Sleep duration between orders: {sleep_duration} seconds")

    start_time = datetime.now()

    while True:
        with grpc.insecure_channel(order_service_url) as channel:
            stub = order_service_pb2_grpc.OrderServiceStub(channel)
            orders = fetch_orders(stub)

            if not orders:
                print("No orders to process")
            else:
                print(f"Processing {len(orders)} orders")

                for order in orders:
                    order.status = "Processing"

                    # Send the order to the order service
                    serialized_order = order.SerializeToString()
                    print(f"Order {order.id} processed with status {order.status}. {serialized_order}")

        time.sleep(sleep_duration)

if __name__ == '__main__':
    main()