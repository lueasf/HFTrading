import asyncio
import string
from collections import defaultdict

import schedule
from prometheus_client import start_http_server, Gauge

import nats_py

# collect data, connect to nats (with nats.py) and expose it to prometheus

# Create a metric to track time spent and requests made.
BUY_NUMBER = Gauge('hft_buy_number', 'Buy number', ['symbol'])
SELL_NUMBER = Gauge('hft_sell_number', 'Sell number', ['symbol'])
LATENCY = Gauge('hft_latency', 'Latency', ['symbol'])

latency_sum = defaultdict(int)
latency_count = defaultdict(int)


def add_order(type: str, labels: dict):
    if type == 'BUY':
        BUY_NUMBER.labels(labels['symbol']).inc()
    elif type == 'SELL':
        SELL_NUMBER.labels(labels['symbol']).inc()


def add_latency(value: string, labels: dict):
    global latency_sum, latency_count
    latency_sum[labels["symbol"]] += int(value)
    latency_count[labels["symbol"]] += 1


def update_latency():
    global latency_sum, latency_count

    for symbol in latency_sum.keys():
        if latency_count[symbol] == 0:
            continue
        LATENCY.labels(symbol).set(latency_sum[symbol] / latency_count[symbol])
        latency_sum[symbol] = 0
        latency_count[symbol] = 0


def deserialize(data):
    value = data.split("\n")[0]
    labels_str = data.split("\n")[1]
    labels = {}
    for label in labels_str.split(","):
        if label:
            k, v = label.split("=")
            labels[k] = v.strip("\"")
    return value, labels


def exec_message(subject, data):
    # we'll see when there are other types of messages
    data_deserialized = deserialize(data)
    if subject == "orders":
        add_order(data_deserialized[0], data_deserialized[1])
    elif subject == "latency":
        add_latency(data_deserialized[0], data_deserialized[1])


def reset_order():
    BUY_NUMBER.clear()
    SELL_NUMBER.clear()


async def test():
    schedule.every(15).seconds.do(update_latency)

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

    asyncio.run(main())  # run NATS and HTTP server
