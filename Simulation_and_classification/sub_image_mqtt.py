import paho.mqtt.client as mqtt
MQTT_SERVER = "localhost"
TOPICS = ["Status", "Tachometer", "UnderhangAX_plot", "UnderhangRa_plot_", "UnderhangTa_plot", 
                    "OverhangAx_plot", "OverhangRa_plot", "OverhangTa_plot", "Microphone_plot"]


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(TOPICS[0])

    # connect in all topics
    # for i in range (len(TOPICS)):
    #     client.subscribe(TOPICS[i])


def on_message(client, userdata, msg):
    # more callbacks, etc
    # Create a file with write byte permission

    f = open(msg.topic + '.jpeg', "wb")
    print(msg.payload)
    f.write(msg.payload)
    print("Image Received")
    f.close()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)
client.loop_forever()