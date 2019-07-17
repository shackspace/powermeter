import paho.mqtt.client as mqtt
import sys
from datetime import datetime
from serial import *

import re
regexPower = re.compile("[+][0-9]+[*]")
regexCurrent = re.compile("[0-9.]+[*]A")
regexVoltage = re.compile("[0-9.]+[*]V")
regexReading = re.compile("1-0:1\.8\..\*255\(([0-9.]+)\)")
regexSerial = re.compile("1-0:0\.0\.0\*255\(([0-9]+)\)")
regexEpochTime = re.compile("[0-9]+")

serialMapper = {
    "20745965": "total",
    "12313":"rz"
}

def main():
    client = mqtt.Client()
    broker_url = "mqtt.shack"
    broker_port = 1883
    def on_connect(client,userdata,flags,rc):
        print("connection successful")
        client.publish("/power/lwt",payload="Online", qos=0, retain=True)
        for meterId,meter in serialMapper.items():
            print(f"/power/mapper/{meterId} = {meter}")
            client.publish(f"/power/mapper/{meterId}", payload=meter,retain=True)

    def on_disconnect(client,userdata,rc):
        if rc != 0:
            print("Unexpected MQTT disconnection. Will auto-reconnect")

    def storeSensorValueInMQTT(client, meter, phase, typ, value):
            print(f"/power/{meter}/L{phase}/{typ} = {value}")
            client.publish(topic=f"/power/{meter}/L{phase}/{typ}", payload=value)


    client.will_set("/power/lwt", payload="Offline", qos=0, retain=True)
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
        try:
            currents = [ float(x.strip("*A")) for x in regexCurrent.findall(data) ]
            voltages = [ float(x.strip("*V")) for x in regexVoltage.findall(data) ]
            powerUsage =[ float(x.strip("*+")) for x in regexPower.findall(data) ]
            totalReading = regexReading.search(data).groups()
            meterId = regexSerial.search(data).group(1)

            try:    meter = serialMapper[meterId]
            except: meter = "unknown"


            print(f"Meter {meter} ({meterId})")
            for i in range (0,3):
                storeSensorValueInMQTT(client, meter, 1+i,"Voltage", voltages[i]);
                storeSensorValueInMQTT(client, meter, 1+i,"Current", currents[i]);
                storeSensorValueInMQTT(client, meter, 1+i,"Power",   powerUsage[i]);

            client.publish(topic=f"/power/{meter}/consumed", payload=totalReading[0] )
            print(f"/power/{meter}/consumed = {totalReading[0]}")
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
