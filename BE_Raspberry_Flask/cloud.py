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
	mqtt.subscribe("nusIS5451Plantsense-plant_sensor_data")
	mqtt.subscribe("nusIS5451Plantsense-plant_info")
	mqtt.subscribe("nusIS5451Plantsense-system_sensor_data")
	mqtt.subscribe("nusIS5451Plantsense-last_watered")


def onMessage(client, userdata, msg):
	print(str(msg.payload.decode("utf-8")))
	data = json.loads(msg.payload.decode("utf-8"))
	
	if msg.topic.split("-")[1] == "plant_sensor_data":
		conn = mongo_dba("plant_sensor_data").post_data(data)
  
	if msg.topic.split("-")[1] == "last_watered":
		conn = mongo_dba("plant_info").update_last_watered(data)
  
	if msg.topic.split("-")[1] == "plant_info":
		conn = mongo_dba("plant_info").update_plant_info(data)
  
	if msg.topic.split("-")[1] == "system_sensor_data":
		conn = mongo_dba("system_sensor_data").update_system_data(data)
	 
	 

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

@app.route('/plant_data', methods=['GET'])
def get_plant_data():
	return mongo_dba("plant_data").get_all_data()

@app.route('/camera', methods=['GET'])
def get_camera_picture():
	return "camera picture here"

app.run()