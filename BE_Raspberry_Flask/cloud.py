import ssl
from flask import Flask, request, jsonify, json
from flask_cors import CORS
from paho.mqtt import client as mqttClient
from dba.mongo_dba import mongo_dba
from ml.rain_predictor import rain_predictor

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
	print("MQTT on message! ")
	
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
			pred = rain_predictor().predict(data['temp'], data['humidity']) 
			mqtt.publish("nusIS5451Plantsense-prediction", str(json.dumps(
			{"result": pred}))) # ------------ REVIEW THIS

			# Test output (yes)
			#print("rain prediction triggered")
			#mqtt.publish("nusIS5451Plantsense-prediction", str(json.dumps(
			#{"rain_result": "yes"}))) # ------------ REVIEW THIS
   
   			# Test output (no)
			#mqtt.publish("nusIS5451Plantsense-prediction", str(json.dumps(
			#{"result": "no"}))) # ------------ REVIEW THIS
   
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
@app.route('/all', methods=['GET'])
def get_all():
	sensor_values = mongo_dba("plant_sensor_data").get_last_sensor_values()
	tank_level = mongo_dba("water_tank").get_water_tank_level()
	weather = mongo_dba("weather").get_last_weather_data()
	plants = mongo_dba("plant_info").get_all_plant_info()
 
	return json.dumps({"plant_sensor_data": sensor_values, "water_tank": tank_level, "weather": weather, "plants_info": plants})

@app.route('/sensor_values', methods=['GET'])
def get_sensor_values():
	sensor_values = mongo_dba("plant_sensor_data").get_last_sensor_values()
	tank_level = mongo_dba("water_tank").get_water_tank_level()
	weather = mongo_dba("weather").get_last_weather_data()
 
	return json.dumps({"plant_sensor_data": sensor_values, "water_tank": tank_level, "weather": weather})

@app.route('/plants_info', methods=['GET'])
def get_plant_data():
	return json.dumps(mongo_dba("plant_info").get_all_plant_info())

@app.route('/camera', methods=['GET'])
def get_camera_picture():
	return "camera picture here"

@app.route('/water_tank', methods=['GET'])
def get_water_tank_level():
	return json.dumps(mongo_dba("water_tank").get_water_tank_level())


@app.route('/plant_info', methods=['POST'])
def update_pant_info():
	data = request.form['data']
	data = json.loads(data)
	print(str(data))
	res = mongo_dba("plant_info").update_plant_info(data)
 
	return str(res)




app.run()