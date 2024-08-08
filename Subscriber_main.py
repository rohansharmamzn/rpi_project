import json
import os
import time
from datetime import datetime
import paho.mqtt.client as mqtt

# Configuration
broker_address = "your_mqtt_broker_address"
broker_port = 1883
mqtt_topic = "your/topic/here"
threshold = 30.0  # Example threshold in degrees Celsius
duration_threshold = 300  # 5 minutes = 300 seconds
output_file = "sensor_data.txt"

# State variables
crossed_threshold = False
start_time = None

# Callback function when a message is received
def on_message(client, userdata, message):
    global crossed_threshold, start_time

    try:
        # Decode the incoming message
        payload = message.payload.decode("utf-8")
        print(f"Received message: {payload} on topic {message.topic}")

        # Parse the payload (assuming JSON format, adjust as needed)
        sensor_data = json.loads(payload)
        temperature = sensor_data.get("temperature")

        if temperature is not None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sensor_data['timestamp'] = timestamp  # Add timestamp to the data
            
            # Save data locally with a timestamp
            save_data(sensor_data)

            # Compare the temperature with the threshold
            if temperature > threshold:
                if not crossed_threshold:
                    # Start the timer if the threshold is crossed for the first time
                    crossed_threshold = True
                    start_time = time.time()
                    print(f"Threshold crossed at {timestamp}. Monitoring for continuous exceedance.")
                else:
                    # Check if the threshold has been crossed continuously for 5 minutes
                    elapsed_time = time.time() - start_time
                    if elapsed_time >= duration_threshold:
                        raise_alarm(sensor_data)
            else:
                # Reset the monitoring if the temperature drops below the threshold
                crossed_threshold = False
                start_time = None
                print(f"Temperature {temperature}°C dropped below the threshold. Monitoring reset.")
        else:
            print("Temperature data not found in the message.")

    except Exception as e:
        print(f"Error processing message: {e}")

# Function to save data locally
def save_data(data):
    with open(output_file, "a") as file:
        file.write(json.dumps(data) + "\n")
    print(f"Data saved: {data}")

# Function to raise an alarm
def raise_alarm(data):
    print(f"ALARM! Continuous threshold exceedance detected: {data}")
    # we can add alarm handling code here, e.g. trigger a buzzer

# Initialize MQTT client
client = mqtt.Client()

# Set callback function
client.on_message = on_message

# Connect to MQTT broker
client.connect(broker_address, broker_port, 60)

# Subscribe to the topic
client.subscribe(mqtt_topic)
print(f"Subscribed to topic {mqtt_topic}")

# Start the loop to process received messages
client.loop_forever()
