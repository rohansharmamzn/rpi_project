#Use below line to install DHT sensor liberary
# pip install paho-mqtt Adafruit_DHT
#Code by Rohan sharma
import time
import paho.mqtt.client as mqtt
import Adafruit_DHT

# MQTT configuration
broker_address = "your_mqtt_broker_address"   #this is example address
broker_port = 1883                            #this is port number
mqtt_topic = "your/topic/here"                #this is example topic

# Sensor configuration (DHT11 )
sensor = Adafruit_DHT.DHT11
sensor_pin = 4    # GPIO pin where the sensor is connected

# Function to read temperature from the sensor
def read_temperature():
    temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)
    if temperature is not None:
        return temperature
    else:
        print("Failed to retrieve data from sensor")
        return None

# Function to publish temperature to MQTT broker
def publish_temperature(client, temperature):
    client.publish(mqtt_topic, temperature)
    print(f"Published {temperature}°C to {mqtt_topic}")

# Initialize MQTT client
client = mqtt.Client()
client.connect(broker_address, broker_port, 60)

# Main loop 
try:
    while True:
        temperature = read_temperature()
        if temperature is not None:
            publish_temperature(client, temperature)
        time.sleep(60)  # sleep time is 60s as mentioned in given problem
except KeyboardInterrupt:
    print("Program interrupted")
finally:
    client.disconnect()
    print("MQTT client disconnected")
