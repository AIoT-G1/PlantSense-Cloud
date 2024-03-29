import ssl
from flask import Flask, request, jsonify, json, render_template, redirect, url_for
from flask_cors import CORS
from paho.mqtt import client as mqttClient
from dba.mongo_dba import mongo_dba
from joblib import load
import joblib
import sklearn
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from teleflask import Teleflask

# Email
from flask_mail import Mail,  Message

import socket

#   Init Flask Server   #
app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = False

host_addr = "172.25.107.100"

mqtt = None
picture_url = []

#   Init MQTT Client   #


def onConnect(client, userdata, flags, rc):
    # MQTT topics to subscribe
    mqtt.subscribe("nusIS5451Plantsense-plant_sensor_data")
    mqtt.subscribe("nusIS5451Plantsense-plant_info")
    mqtt.subscribe("nusIS5451Plantsense-weather")
    mqtt.subscribe("nusIS5451Plantsense-water_tank")


# Init Flask Mail #
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'plantsense.aiot@gmail.com'
app.config['MAIL_PASSWORD'] = 'bnztzvlpgxueoxye'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# Init PlantSense Telegram Bot (@PlantSenseBot) #
# bot = Teleflask("6189463418:AAGvNioYlyqk8jxPQsBBQRHbRFoJRIhksN8")
# bot.init_app(app)
# bot.bot.send_message('@rxmxdhan', 'It works :D')  # please don't spam me :D
# use bot from initialize above
# from teleflask.messages import TextMessage

# python3 -m teleflask.proxy --https api_key=6189463418:AAGvNioYlyqk8jxPQsBBQRHbRFoJRIhksN8 host=127.0.0.1 port=5000


def manage_image_chunks(data):
    if data['action'] == "update_last_image_1":
        picture_url = []
        picture_url.append(data['photo_url'])

    if data['action'] == "update_last_image_2" or data['action'] == "update_last_image_3" or data['action'] == "update_last_image_4":
        picture_url.append(data['photo_url'])

    if data['action'] == "update_last_image_5":
        print(str(data))
        url = ""
        picture_url.append(data['photo_url'])

        for photo in picture_url:
            url += photo

        data['photo_url'] = url
        print(url)
        conn = mongo_dba("plant_info").update_last_image(data, 2)


def onMessage(client, userdata, msg):
    print(str(msg.payload.decode("utf-8")))
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

        if data['action'] == "update_last_disease":
            conn = mongo_dba("plant_info").update_last_disease(data)

        if data['action'] == "update_last_image_1":
            print(str(data))
            manage_image_chunks(data)

    # Weather conditions (timestamp, temp, humidity)
    if msg.topic.split("-")[1] == "weather":
        print("rain prediction triggered")
        if data['action'] == "predict":
            clf = joblib.load('rain-classifier.joblib')
            temperature = data['temp']
            humidity = data['humidity']
            print(clf)

            print("to predict --> temp: " +
                  str(temperature) + " ; humidity: " + str(humidity))
# temperature, humidity
            newX = [[temperature, humidity]]
            result = clf.predict(newX)
            print('Predict Rain: temp={}; humidity={}; rain={}'.format(
                temperature, humidity, result[0]))
            # pred = rain_predictor().predict(data['temp'], data['humidity'])
            # print(pred)
            mqtt.publish("nusIS5451Plantsense-prediction", str(json.dumps(
                {"result": result[0].lower()})))  # ------------ REVIEW THIS

        if data['action'] == "add_weather_data":
            conn = mongo_dba("weather").add_weather_data(data)

    # Water tank level (level)
    if msg.topic.split("-")[1] == "water_tank":
        conn = mongo_dba("water_tank").update_water_tank(data)

        # Check if less than or equal to 20%, then send Email notification
        tank_level = data['tank_level']
        if (float(tank_level) < 0.2):
            percent = str(int(float(tank_level)*100)) + "%"
            # print("percent: " + percent)
            send_mail_water_tank(percent)
            send_telegram_tank(percent)


mqtt = mqttClient.Client()
mqtt.on_connect = onConnect
mqtt.on_message = onMessage

mqtt.tls_set(ca_certs="certs/mosquitto.org.crt", certfile="certs/client.crt",
             keyfile="certs/client.key", tls_version=ssl.PROTOCOL_TLSv1_2)
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

    return str("OK")


@app.route('/plant_info/upload_image', methods=['POST'])
def upload_image():
    data = request.form['data']
    data = json.loads(data)

    print(str(data))

    return "OK"

# Flask Email #
# @app.route('/send/') # testing


def send_mail_water_tank(percent):
    with app.app_context():
        print("send_mail_water_tank()")
        title = "PlantSense Alert: Low Water Tank Level!"
        recipient = "plantsense.aiot@gmail.com"

        msg = mail.send_message(
            title,
            sender='plantsense.aiot@gmail.com',
            recipients=[recipient],
            html="Hello,<br><br>The water tank level has fallen below 20%. Currently, it is at " + percent +
            " according to our records. <br><br>Immediate action is required to top up the water level in order to ensure the proper operation of the PlantSense system.<br><br>Your Smart Assistant,<br>PlantSense"
        )
        return 'Mail sent'


def send_mail_disease(plantName):
    with app.app_context():
        print("send_mail_disease()")
        title = "PlantSense Alert: Disease Detected!"
        recipient = "plantsense.aiot@gmail.com"

        msg = mail.send_message(
            title,
            sender='plantsense.aiot@gmail.com',
            recipients=[recipient],
            html="Hello,<br><br>We would like to inform you that a disease has been detected on Plant " + plantName +
            ". <br><br>. Immediate action and extra care for the plant are required to mitigate the situation.<br><br>As your trusted Smart Assistant, PlantSense urges you to take prompt measures to address the issue and safeguard the health of the plant. Timely intervention can help prevent further damage and ensure the well-being of your beloved plant.<br><br>Your Smart Assistant,<br>PlantSense"
        )
        return 'Mail sent'


def send_telegram_tank(percent):
    chat_id = "-1001696530800"
    api_key = "6088592232:AAG1laK2NXXq9uxJiLB6DJ8oaXElQrfl6QQ"

    message = "Hello. The water tank level has fallen below 20%. Currently, it is at " + percent + \
        " according to our records. Immediate action is required to top up the water level in order to ensure the proper operation of the PlantSense system. Your Smart Assistant, PlantSense"

    url = f'https://api.telegram.org/bot{api_key}/sendMessage?chat_id={chat_id}&text={message}'
    print(requests.get(url).json())  # this sends the message


def send_telegram_disease(plantName):
    chat_id = "-1001696530800"
    api_key = "6088592232:AAG1laK2NXXq9uxJiLB6DJ8oaXElQrfl6QQ"

    message = "Hello, we would like to inform you that a disease has been detected on Plant " + plantName + \
        ". Immediate action and extra care for the plant are required to mitigate the situation. As your trusted Smart Assistant, PlantSense urges you to take prompt measures to address the issue and safeguard the health of the plant. Timely intervention can help prevent further damage and ensure the well-being of your beloved plant. Your Smart Assistant,PlantSense"

    url = f'https://api.telegram.org/bot{api_key}/sendMessage?chat_id={chat_id}&text={message}'
    print(requests.get(url).json())  # this sends the message


#   Telegram Bot API via TeleFlask   #
# Register the /start command
# @bot.command("start")
# def start(update, text):
# 	# update is the update object. It is of type pytgbot.api_types.receivable.updates.Update
# 	# text is the text after the command. Can be empty. Type is str.
# 	return TextMessage("<b>Hello!</b> Thanks for using @" + bot.username + "!", parse_mode="html")
# # end def

# @bot.command("test")
# def test(update, text):
# 	return "You tested with {arg!r}".format(arg=text)
# end def

# register a function to be called for updates.
# @bot.on_update
# def foo(update):
# 	from pytgbot.api_types.receivable.updates import Update
# 	assert isinstance(update, Update)
# 	# do stuff with the update
# 	# you can use bot.bot to access the pytgbot.Bot's messages functions
# 	if not update.message:
# 		return
# 		# you could use @bot.on_message instead of this if.
# 	# end if
# 	if update.message.new_chat_member:
# 		return TextMessage("Welcome!")
    # end if
# end def


# Other members to run local
app.run(host=host_addr, port="5000")

# Jaume's main server
# app.run(host=host_addr, port = "5000")
