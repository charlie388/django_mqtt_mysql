from django.conf import settings
import paho.mqtt.client as mqtt
import random
from myapp.models import Upload

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
    # device = device.replace('"','\\"')
    # upload = upload.replace('"','\\"')

    unit = Upload.objects.create(device=device, upload=upload)
    unit.save()
    # sql = f'INSERT INTO iotdb.upload(device, upload) VALUES("{device}", "{upload}");'
    # print(sql)
    # mycursor.execute(sql)
    # mydb.commit()

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
