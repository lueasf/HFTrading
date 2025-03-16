import asyncio
import nats

# Connect to NATS and listen for messages. When a message is received, call func
async def start_nats(func):
    nc = await nats.connect("localhost")

    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()

        # call exporter
        func(subject, data)

    # subscribe to subject and exec message_handler which call func which 
    # call exec_message from exporter.py
    subjects = ["orders", "latency"]
    for subject in subjects:
        await nc.subscribe(subject, cb=message_handler)

    # just wait

    while True:
        await asyncio.sleep(1000)