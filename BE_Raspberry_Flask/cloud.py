from flask import Flask, request, jsonify, json
from flask_cors import CORS
from paho.mqtt import client as mqttClient
import ssl

#   Init Flask Server   #
app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = False

mqtt = None 

#   Init MQTT Client   #
def onConnect(client, userdata, flags, rc):
	# MQTT topics to subscribe
	mqtt.subscribe("nus_IS5451_Plantsense_global_sensor_data")
	mqtt.subscribe("nus_IS5451_Plantsense_plant_disease")
	mqtt.subscribe("nus_IS5451_Plantsense_buggy_state")


def onMessage(client, userdata, msg):
	print(str(msg.payload.decode("utf-8")))
	#data = json.loads(str(msg.payload.decode("utf-8")))
	#print(str(data))

mqtt = mqttClient.Client()
mqtt.on_connect = onConnect
mqtt.on_message = onMessage

mqtt.tls_set(ca_certs="certs/mosquitto.org.crt", certfile="certs/client.crt", keyfile="certs/client.key", tls_version=ssl.PROTOCOL_TLSv1_2)
#mqtt.username_pw_set(username="rw", password="readwrite")
mqtt.connect("test.mosquitto.org", 8883)
mqtt.loop_start()


#   Server API   #

# Obtener valores más recientes almacenados en BBDD
@app.route('/sensor_values', methods=['GET'])
def get_sensor_values():
	return "sensor values here"

@app.route('/camera', methods=['GET'])
def get_camera_picture():
	return "camera picture here"

app.run()