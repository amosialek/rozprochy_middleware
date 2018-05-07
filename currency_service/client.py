import grpc

from currencyInfo_pb2 import Empty
from currencyInfo_pb2_grpc import CurrencyInfoStreamStub

channel = grpc.insecure_channel('localhost:50052')

currency_info_stub = CurrencyInfoStreamStub(channel)
for currency_info in currency_info_stub.getCurrencyInfo(Empty()):
    print(currency_info)
