from flask import Flask, request, jsonify, json
from flask_cors import CORS
from paho.mqtt import client as mqttClient
from mongo_dba import mongo_dba
import ssl

#   Init Flask Server   #
app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = False

mqtt = None 

#   Init MQTT Client   #
def onConnect(client, userdata, flags, rc):
	# MQTT topics to subscribe
	mqtt.subscribe("nusIS5451Plantsense-global_sensor_data")
	mqtt.subscribe("nusIS5451Plantsense-plant_disease")
	mqtt.subscribe("nusIS5451Plantsense-watering_system")


def onMessage(client, userdata, msg):
	print(str(msg.payload.decode("utf-8")))
	data = json.loads(str(msg.payload.decode("utf-8")))
	print(str(data))
	
	# retrieve topic and send to the collection
	conn = mongo_dba(msg.topic.split("-")[1])
	conn.post_data(data)
     
     

mqtt = mqttClient.Client()
mqtt.on_connect = onConnect
mqtt.on_message = onMessage

mqtt.tls_set(ca_certs="certs/mosquitto.org.crt", certfile="certs/client.crt", keyfile="certs/client.key", tls_version=ssl.PROTOCOL_TLSv1_2)
#mqtt.username_pw_set(username="rw", password="readwrite")
mqtt.connect("test.mosquitto.org", 8883)
mqtt.loop_start()


#   Server API   #

@app.route('/sensor_values', methods=['GET'])
def get_sensor_values():
	return mongo_dba("sensor_values").get_last_sensor_values()

@app.route('/camera', methods=['GET'])
def get_camera_picture():
	return "camera picture here"

app.run()