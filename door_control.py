import paho.mqtt.client as mqtt

# MQTT Broker settings
BROKER = "localhost"  # Replace with your MQTT broker address (e.g., localhost or IP)
PORT = 1883                  # Default MQTT port for unencrypted connections
TOPIC = "iot/door_control"   # Replace with the topic you want to subscribe to

# Callback when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        client.subscribe(TOPIC)
        print(f"Subscribed to topic: {TOPIC}")
    else:
        print(f"Connection failed with code {rc}")

# Callback when a message is received
def on_message(client, userdata, msg):
    print(f"Message received from topic '{msg.topic}': {msg.payload.decode()}")

# Create MQTT client
client = mqtt.Client()

# Assign callback functions
client.on_connect = on_connect
client.on_message = on_message

try:
    # Connect to the MQTT broker
    client.connect(BROKER, PORT)

    # Start the network loop to handle communication with the broker
    client.loop_forever()

except KeyboardInterrupt:
    print("Exiting...")
    client.disconnect()
import paho.mqtt.client as mqtt

BROKER = "localhost"
TOPIC = "iot/door_control"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    print(f"Message received: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER)
client.loop_forever()
