import grpc
from concurrent import futures
import worker_pb2
import worker_pb2_grpc

class WorkerService(worker_pb2_grpc.WorkerServiceServicer):
    def ProcessOrder(self, request, context):
        # Simulate order processing logic
        print(f"[INFO] Processing Order: {request.order_id} for Customer: {request.customer_id}")
        total_price = sum(item.quantity * item.price for item in request.items)

        # Logic for order processing
        if total_price > 0:
            print(f"[INFO] Order {request.order_id} processed successfully. Total: ${total_price:.2f}")
            return worker_pb2.OrderResponse(
                order_id=request.order_id,
                success=True,
                message=f"Order processed. Total: ${total_price:.2f}"
            )
        else:
            print(f"[ERROR] Invalid order {request.order_id}")
            return worker_pb2.OrderResponse(
                order_id=request.order_id,
                success=False,
                message="Invalid order."
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    worker_pb2_grpc.add_WorkerServiceServicer_to_server(WorkerService(), server)
    server.add_insecure_port('[::]:50051')
    print("[INFO] gRPC Worker Server started on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
