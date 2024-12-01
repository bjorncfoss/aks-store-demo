import grpc
import os
import logging
import signal
from concurrent import futures
from grpc_health.v1 import health, health_pb2, health_pb2_grpc

import worker_pb2
import worker_pb2_grpc

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WorkerService(worker_pb2_grpc.WorkerServiceServicer):
    def ProcessOrder(self, request, context):
        try:
            logging.info(f"Processing Order: {request.order_id} for Customer: {request.customer_id}")
            total_price = sum(item.quantity * item.price for item in request.items)

            if total_price > 0:
                logging.info(f"Order {request.order_id} processed successfully. Total: ${total_price:.2f}")
                return worker_pb2.OrderResponse(
                    order_id=request.order_id,
                    success=True,
                    message=f"Order processed. Total: ${total_price:.2f}"
                )
            else:
                logging.error(f"Invalid order {request.order_id}")
                return worker_pb2.OrderResponse(
                    order_id=request.order_id,
                    success=False,
                    message="Invalid order."
                )
        except Exception as e:
            logging.error(f"Error processing order {request.order_id}: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("An error occurred while processing the order.")
            return worker_pb2.OrderResponse(
                order_id=request.order_id,
                success=False,
                message="Internal server error."
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    worker_pb2_grpc.add_WorkerServiceServicer_to_server(WorkerService(), server)
    
    # Add health service
    health_servicer = health.HealthServicer()
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
    health_servicer.set('', health_pb2.HealthCheckResponse.SERVING)

    port = os.getenv("GRPC_SERVER_PORT", "50051")
    server.add_insecure_port(f'[::]:{port}')
    logging.info(f"gRPC Worker Server started on port {port}")
    
    def handle_shutdown(signum, frame):
        logging.info("Shutting down gRPC server...")
        server.stop(0)
        logging.info("gRPC server stopped.")
    
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)

    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
