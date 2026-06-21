import paho.mqtt.client as mqtt
import time
import datetime
import json

BASE = "/data"

# Load configs from a JSON file
with open(f"{BASE}/config.json") as fd:
    config = json.load(fd)

# The MQTT broker to connect to
broker_address = config["BROKER_ADDRESS"] #"broker.mqtt-dashboard.com"
broker_port = int(config["BROKER_PORT"]) #1883

# The MQTT topics to subscribe/publish to
subscribe_topic = config["SUBSCRIBE_TOPIC"]
publish_topic = config["PUBLISH_TOPIC"]

# The last known state of each zone
last_state = ['0', '0', '0', '0', '0']
resync_state = [False, False, False, False, False]

# The MQTT client object
client = mqtt.Client()

# Empty/Inicial schedule
schedule = []

def load_schedule():
    # Load the watering schedule from a JSON file
    # Json example
    #[
    #    {"zone": 1, "day": [0, 1, 2, 3, 4, 5, 6], "start_time": "9:43", "duration": 120}
    #]
    global schedule
    with open(f"{BASE}/schedule.json") as f:
        schedule = json.load(f)
    print(schedule)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe(subscribe_topic)


def on_message(client, userdata, msg):
    print("Reply Message "+str(msg.payload.decode()))
    if msg.topic == subscribe_topic:
        zones = msg.payload.decode().split()[:5]
        print("Zones "+str(zones))
        print("Last State "+str(last_state))
        for i in range(5):
            if last_state[i] != zones[i]:
                global resync_state
                resync_state[i] = True


def publish_command(client, index, state):
    topic = publish_topic
    zone = index + 1
    message = f"R{zone}_{state}"
    print("Publish "+str(message))
    client.publish(topic, message)


# Connect to the MQTT broker and start the MQTT client loop
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, broker_port, 60)
client.loop_start()

# The main loop that schedules watering based on the predefined schedule
loadScheduleCounter = 0
while True:
    now = datetime.datetime.now()  # create a datetime object from the current time

    print(now)
    if (loadScheduleCounter == 0):
        load_schedule()
        loadScheduleCounter = 12 # every minute force reload
    loadScheduleCounter -= 1

    for item in schedule:
        print(now.weekday())
        print(now.strftime("%k:%M").lstrip())
        print(item["start_time"])

        if now.weekday() in item["day"] and now.strftime("%k:%M").lstrip() == item["start_time"].lstrip():
            publish_command(client, item["zone"]-1, "ON")
            last_state[item["zone"]-1] = '1'
        if now.weekday() in item["day"]:
            end_time = datetime.datetime.strptime(item["start_time"], '%H:%M').time()
            end_datetime = datetime.datetime.combine(now.date(), end_time) + datetime.timedelta(seconds=item["duration"])
            end_datetime2 = datetime.datetime.combine(now.date(), end_time) + datetime.timedelta(seconds=item["duration"]+60)
            if (now >= end_datetime) and (now <= end_datetime2):
                publish_command(client, item["zone"]-1, "OFF")
                last_state[item["zone"]-1] = '0'
    for i in range(5):
        print("resync_state"+str(resync_state))
        if resync_state[i] == True:
            resync_state[i] = False
            if last_state[i] == '1':
                publish_command(client, i, "ON")
            else:
                publish_command(client, i, "OFF")
    time.sleep(5)
