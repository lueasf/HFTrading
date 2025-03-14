import asyncio
import nats

async def start_nats(func):
    nc = await nats.connect("localhost")

    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()

        func(data)

        print("Received a message on '{subject} {reply}': {data}".format(
            subject=subject, reply=reply, data=data))

    # Simple publisher and async subscriber via coroutine.
    sub = await nc.subscribe("foo", cb=message_handler)

    # just wait

    while True:
        await asyncio.sleep(1000)