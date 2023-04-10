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
	mqtt.subscribe("nusIS5451Plantsense-weather")
	mqtt.subscribe("nusIS5451Plantsense-water_tank")


def onMessage(client, userdata, msg):
	data = json.loads(msg.payload.decode("utf-8").replace("'", "\""))
	
	# Plant sensor data (timestamp, moisture, light, plant_node_id...)
	if msg.topic.split("-")[1] == "plant_sensor_data":
		conn = mongo_dba("plant_sensor_data").add_plant_sensor_data(data)
  
	# Plant information (node_id, , name, desc, disease, last_watered...)
	if msg.topic.split("-")[1] == "plant_info":
     
		if data['action'] == "update_plant":
			conn = mongo_dba("plant_info").update_plant_info(data)
   
		if data['action'] == "update_last_watered":
			conn = mongo_dba("plant_info").update_last_watered(data)
  
	# Weather conditions (timestamp, temp, humidity)
	if msg.topic.split("-")[1] == "weather":
     
		if data['action'] == "predict":
			# Predict rain :) -------------------- REVIEW THIS
			pass
			mqtt.publish("nusIS5451Plantsense-prediction", str(json.dumps(
			{"result": "YES/NO"}))) # ------------ REVIEW THIS
   
		if data['action'] == "add_weather_data":
			conn = mongo_dba("weather").add_weather_data(data)
   
	# Water tank level (level)
	if msg.topic.split("-")[1] == "water_tank":
			conn = mongo_dba("water_tank").update_water_tank(data)
	 
	 

mqtt = mqttClient.Client()
mqtt.on_connect = onConnect
mqtt.on_message = onMessage

mqtt.tls_set(ca_certs="certs/mosquitto.org.crt", certfile="certs/client.crt", keyfile="certs/client.key", tls_version=ssl.PROTOCOL_TLSv1_2)
mqtt.connect("test.mosquitto.org", 8883)
mqtt.loop_start()


#   Server API   #

@app.route('/sensor_values', methods=['GET'])
def get_sensor_values():
	return json.dumps(mongo_dba("sensor_values").get_last_sensor_values())

@app.route('/plants_info', methods=['GET'])
def get_plant_data():
	return json.dumps(mongo_dba("plant_info").get_all_plant_info())

@app.route('/camera', methods=['GET'])
def get_camera_picture():
	return "camera picture here"

@app.route('/water_tank', methods=['GET'])
def get_water_tank_level():
    return json.dumps(mongo_dba("water_tank").get_water_tank_level())
app.run()