import paho.mqtt.client as mqtt
import json
import subprocess
import time
import picamera
import os
import datetime
from slacker import Slacker
import configparser
from os import path
import RPi.GPIO as GPIO
import atexit
from operator import itemgetter
import requests

inifile = configparser.ConfigParser()
APP_ROOT = path.dirname(path.abspath(__file__)) + "/"

inifile.read(APP_ROOT + 'config.ini', 'UTF-8')

TOKEN = inifile.get('beebotte', 'token')
HOSTNAME = "mqtt.beebotte.com"
PORT = 8883
USERNAME = inifile.get('beebotte', 'username')
TOPIC = inifile.get('beebotte', 'topic')
CACERT = APP_ROOT + "mqtt.beebotte.com.pem"

N = int(inifile.get('GPIO', 'PIN1'))
n = int(inifile.get('GPIO', 'PIN2'))
led_list = [N, n]
        
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_list, GPIO.OUT)
GPIO.output(led_list, GPIO.LOW)

filelists = []
for file in os.listdir():
    base,ext = os.path.splitext(file)
    if ext == '.jpg':
        # getctime はfileが最後に変更された日時を示す
        # カレントディレクトリのjpgを取得時刻とリストした状態でfilelistsにappendしてやっている
        filelists.append([file, os.path.getctime(file)])
    filelists.sort(key = itemgetter(1), reverse = True)
    MAX_CNT = 0
    for i, file in enumerate(filelists):
        if i > MAX_CNT -1:
            os.remove(file[0])
            print('delete jpg files')

GPIO.output(n, GPIO.HIGH)
time.sleep(1)
GPIO.output(n, GPIO.LOW)

def on_connect(client, userdata, flags, respons_code):
    print('status0'.format(respons_code))
    client.subscribe(TOPIC)
    
GPIO.output(n, GPIO.HIGH)
time.sleep(1)
GPIO.output(n, GPIO.LOW)
    
def on_message(client, userdata, msg):
    print(msg.topic + "" + str(msg.payload))
    data = json.loads(msg.payload.decode("utf-8"))["data"][0]
    data = {key:value.strip() for key, value in data.items()}
    if "photo" in data.keys():
        # 写真を撮っている部分
        # with picamera.PiCamera() as camera:
        #     camera.resolution = (1920, 1080)
        #     camera.rotation = inifile.get('camera', 'rotation')
        #     camera.start_preview()
        #     #camera warm-up time
        #     now = datetime.datetime.now()
        #     picture = inifile.get('room','room') + "({0:%Y-%m-%d %H:%M:%S})".format(now) +".jpg"
        #     camera.capture(picture)
        #
        now = datetime.datetime.now()
        # ファイル名
        picture = APP_ROOT + inifile.get('room', 'room') + "({0:%Y-%m-%d %H:%M:%S})".format(now) + ".jpeg"
        # cv2.imwrite(picture, img)
        cmd = "chmod +x run.sh".split()
        subprocess.call(cmd)
        cmd = "./takeshot.sh {}".format(picture)
        cmd = cmd.split()
        subprocess.call(cmd)

        GPIO.output(N, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(N, GPIO.LOW)
        
        
        channel = inifile.get('slacker', 'channel')
        Token = inifile.get('slacker', 'token')
        filename = str(picture)
        
        files = {"file": open(picture, "rb")}
        param = {
                "token" : Token,
                "channels" : channel,
                "filename" : filename,
                "initial_comment" : "IP ADDR: " + inifile.get('slacker', 'ip')
                }
        requests.post(url="https://slack.com/api/files.upload", params=param, files=files)

        os.remove(picture)
        
        for i in range(2):
            GPIO.output(N, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(N, GPIO.LOW)
            time.sleep(0.5)
            
try:
    client = mqtt.Client()
    client.username_pw_set("token:%s"%TOKEN)
    client.on_connect = on_connect
    client.on_message = on_message
    client.tls_set(CACERT)
    client.connect(HOSTNAME, port=PORT, keepalive=60)
    client.loop_forever()
    
except KeyboardInterrupt:
    GPIO.cleanup()
    print("cancel")
    
finally:
    print("end")