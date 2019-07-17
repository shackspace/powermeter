import paho.mqtt.client as mqtt
import sys
from datetime import datetime
from serial import *


def main():
    client = mqtt.Client()
    broker_url = "mqtt.shack"
    broker_port = 1883
    def on_connect(client,userdata,flags,rc):
        print("connection successful")
        client.publish("/powerraw/lwt",payload="Online", qos=0, retain=True)

    def on_disconnect(client,userdata,rc):
        if rc != 0:
            print("Unexpected MQTT disconnection. Will auto-reconnect")

    client.will_set("/powerraw/lwt", payload="Offline", qos=0, retain=True)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    print(f"Connecting to mqtt broker {broker_url}:{broker_port}")
    client.connect(broker_url, broker_port,60)


    baudrate=9600
    port="/dev/ttyUSB0"
    print(f"Connecting to serial {port}@{baudrate} baud")
    ser = Serial(baudrate=baudrate,port=port,parity=PARITY_EVEN,bytesize=SEVENBITS)
    while client.loop() == 0:
        data = ser.read_until(b'!',2048).decode().lstrip()
        client.publish(topic="/powerraw/data",payload=data,qos=0,retain=False)
        #print(data)
        #sys.stdout.write('.',)
        #sys.stdout.flush()

if __name__ == "__main__":
    main()
