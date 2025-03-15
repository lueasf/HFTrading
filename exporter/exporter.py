from prometheus_client import start_http_server, Summary, Gauge
import random
import time
import asyncio
import schedule
import nats_py

# Create a metric to track time spent and requests made.
REQUEST_TIME = Gauge('request_processing_seconds', 'Time spent processing request')
BUY_NUMBER = Gauge('buy_number', 'Buy number')
SELL_NUMBER = Gauge('sell_number', 'Sell number')

def add_order(type: str):
    if type == 'BUY':
        BUY_NUMBER.inc()
    elif type == 'SELL':
        SELL_NUMBER.inc()


def exec_message(data):
    # we'll see when there are other types of messages
    add_order(data)


def reset_order():
    BUY_NUMBER.set(0)
    SELL_NUMBER.set(0)


async def test():
    schedule.every().minute.at(":00").do(reset_order)
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


async def main():
    # Every minute at 0s, reset the buy and sell number
    resetCounterTask = asyncio.create_task(test())

    # bond nats and exec_message
    natsTask = asyncio.create_task(nats_py.start_nats(exec_message))

    await resetCounterTask
    await natsTask

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)

    asyncio.run(main()) # run NATS and HTTP server

