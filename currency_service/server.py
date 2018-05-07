import random
import time
from concurrent import futures

import grpc

import currencyInfo_pb2_grpc
from currencyInfo_pb2 import CurrencyInfo
from currencyInfo_pb2_grpc import add_CurrencyInfoStreamServicer_to_server


def generate_random_number(old_currency_info=None):
    if old_currency_info is None:
        return CurrencyInfo(PLNEUR=random.random()*10,PLNUSD=random.random()*10,PLNCHF=random.random()*10)
    else:
        return CurrencyInfo(PLNEUR=old_currency_info.PLNEUR * random.random() / 50, PLNUSD=old_currency_info.PLNUSD * random.random() / 50, PLNCHF=old_currency_info.PLNCHF * random.random() / 50)

class CurrencyInfoStreamer(currencyInfo_pb2_grpc.CurrencyInfoStreamServicer):
    def getCurrencyInfo(self, request, context):
        number = generate_random_number()
        for i in range(10):
            yield generate_random_number(number)
            time.sleep(1)



def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  add_CurrencyInfoStreamServicer_to_server(CurrencyInfoStreamer(), server)
  server.add_insecure_port('[::]:50052')
  server.start()
  try:
      while True:
          time.sleep(60*60*24)
  except KeyboardInterrupt:
      server.stop(0)


if __name__ == '__main__':
    serve()
