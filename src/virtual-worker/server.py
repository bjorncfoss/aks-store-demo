# server.py
import grpc
from concurrent import futures
import fetch_pb2
import fetch_pb2_grpc

class FetchServiceServicer(fetch_pb2_grpc.FetchServiceServicer):
    def Fetch(self, request, context):
        # Implement your fetch logic here
        result = f"Fetched data for query: {request.query}"
        return fetch_pb2.FetchResponse(result=result)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fetch_pb2_grpc.add_FetchServiceServicer_to_server(FetchServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()