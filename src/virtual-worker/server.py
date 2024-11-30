# server.py
import grpc
from concurrent import futures
import time
import order_service_pb2
import order_service_pb2_grpc

class OrderServiceServicer(order_service_pb2_grpc.OrderServiceServicer):
    def FetchOrders(self, request, context):
        # Example implementation
        orders = [
            order_service_pb2.Order(id=1, status="New"),
            order_service_pb2.Order(id=2, status="New"),
        ]
        return order_service_pb2.FetchOrdersResponse(orders=orders)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_service_pb2_grpc.add_OrderServiceServicer_to_server(OrderServiceServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Server started on port 50052")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()