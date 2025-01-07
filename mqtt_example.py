
import paho.mqtt.client as mqtt
import time
from datetime import datetime
import json

# MQTT Broker Configuration
BROKER = '127.0.0.1'
PORT = 1883
PUBLISH_TOPIC = 'vehicle/speed'
SUBSCRIBE_TOPIC = 'vehicle/speed'

# Publisher
def publisher():
    client = mqtt.Client()
    client.connect(BROKER, PORT, 60)

    for speed in range(0, 100):
        # Get the current timestamp
        timestamp = datetime.utcnow().isoformat()

        # Create message payload
        message = {
            'speed': speed,
            'timestamp': timestamp
        }

        # Publish the message
        client.publish(PUBLISH_TOPIC, json.dumps(message))
        print(f"Published speed: {speed} with timestamp {timestamp}")
        time.sleep(1)

    client.disconnect()
    print("Finished publishing.")

# Subscriber
def on_message(client, userdata, msg):
    received_time = datetime.utcnow()

    # Parse the message
    payload = json.loads(msg.payload.decode())
    speed = payload['speed']
    sent_timestamp = datetime.fromisoformat(payload['timestamp'])

    # Calculate delay
    delay = (received_time - sent_timestamp).total_seconds()
    print(f"Received speed: {speed}, sent at {sent_timestamp}, received at {received_time}, delay: {delay:.3f} seconds")

def subscriber():
    client = mqtt.Client()
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)
    client.subscribe(SUBSCRIBE_TOPIC)

    print("Subscriber is running...")
    client.loop_forever()

if __name__ == "__main__":
    import multiprocessing

    # Run publisher and subscriber in parallel
    publisher_process = multiprocessing.Process(target=publisher)
    subscriber_process = multiprocessing.Process(target=subscriber)

    publisher_process.start()
    subscriber_process.start()

    publisher_process.join()
    subscriber_process.terminate()
