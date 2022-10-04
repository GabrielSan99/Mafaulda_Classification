import paho.mqtt.publish as publish
MQTT_SERVER = "localhost"  #Write Server IP Address
TOPICS = ["Status", "Tachometer", "UnderhangAX_plot", "UnderhangRa_plot_", "UnderhangTa_plot", 
                    "OverhangAx_plot", "OverhangRa_plot", "OverhangTa_plot", "Microphone_plot"]

f=open("python.jpeg", "rb") #3.7kiB in same folder
fileContent = f.read()
byteArr = bytearray(fileContent)


publish.single(TOPICS[0], byteArr, hostname=MQTT_SERVER, retain=True)