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
        func(data)

        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))

    # subscribe to subject and exec message_handler which call func which 
    # call exec_message from exporter.py
    sub = await nc.subscribe("foo", cb=message_handler)

    # just wait

    while True:
        await asyncio.sleep(1000)