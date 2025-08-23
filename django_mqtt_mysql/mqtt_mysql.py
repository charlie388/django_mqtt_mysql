from django.conf import settings
import paho.mqtt.client as mqtt
import random
from myapp.models import Upload
import requests
import json

# 1. go https://developers.line.biz/en/
# 2. go official Line account
# 3. go Messaging API and copy Channel access token 
# token = "Please replace Channel access token from your LINE official account"
token = "xxxxx"
url = "https://api.line.me/v2/bot/message/broadcast"

headers = {
	"Content-Type": "application/json",
	"Authorization": f"Bearer {token}"
}

data = {
	"messages": [
		{ "type": "text",
			"text": ""
		} ]
}

normalTempDuraCnt = 0

def on_connect(mqtt_client, userdata, flags, rc):
    if rc == 0:
        print(f'{my_client_id} Connected MQTT broker successfully')
        mqtt_client.subscribe('+/upload')
    else:
        print('Bad connection. Code:', rc)

def on_message(mqtt_client, userdata, msg):
    device = msg.topic[0: msg.topic.find('/upload')]
    upload = msg.payload.decode('utf-8')
    print(f'device : {device}, upload : {upload}')

    unit = Upload.objects.create(device=device, upload=upload)
    unit.save()

    global normalTempDuraCnt
    upload_obj = json.loads(upload)
    if 'temp' in upload_obj:
        global temp 
        temp = upload_obj['temp']
        if(temp > 50.0 and msg.topic == '01/upload' and normalTempDuraCnt == 0) :
            msg = f'溫度超標 {temp}'
            print(msg)
            data['messages'][0]['text'] = msg
            res = requests.post(url, headers = headers, data = json.dumps(data))
            if res.status_code in (200, 204):
	            print(f"Request fulfilled with response: {res.text}")
            else:
	            print(f"Request failed with response: {res.status_code}-{res.text}")
            normalTempDuraCnt = 10;

        if(temp < 32.0 and normalTempDuraCnt >= 1):
            normalTempDuraCnt -= 1

print("mqtt_mysql.py run")
my_client_id = "web_" + "".join([random.choice("0123456789abcdef") for i in range(8)])
client = mqtt.Client(client_id=my_client_id)
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(
    host=settings.MQTT_SERVER,
    port=settings.MQTT_PORT,
    keepalive=settings.MQTT_KEEPALIVE
)
client.loop_start()
