#!/usr/bin/env python
import asyncio
import paho.mqtt.client as mqtt
data =b""
async def handle_socket(reader,writer):
    global data
    print(f"got connect from {writer.get_extra_info('peername')}")
    writer.write(data)
    await writer.drain()
    print(f"close connection of {writer.get_extra_info('peername')}")
    writer.close()

def main():
    asyncio.run(smain())
async def smain():
    client = mqtt.Client()

    broker_url = "mqtt.shack"
    broker_port = 1883


    def on_connect(client,userdata,flags,rc):
        client.publish("/powersocket/lwt",payload="Online", qos=0, retain=True)
        client.subscribe('/powerraw/data')
    def on_message(client,userdata,message):
        global data
        # print("Received message")
        data = message.payload
        # client.publish(topic="/powersocket/", payload="TestingPayload", qos=1, retain=False)

    client.will_set("/powersocket/lwt", payload="Offline", qos=0, retain=True)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_url, broker_port, 60)
    server = await asyncio.start_server(
        handle_socket , '0.0.0.0', 11111)
    async with server:
        client.loop_start()
        await server.serve_forever()


if __name__ == "__main__":
    main()
