from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django_mqtt_mysql.mqtt_mysql import client
from myapp.models import Upload

def index(request):
    return render(request,"index.html")

def upload(request):
    uploads = Upload.objects.order_by('-id')[:13]
    data = list(uploads.values())
    return JsonResponse(data, safe=False)

def uploadVar(request, id):
    uploads = Upload.objects.filter(id__gt=id).order_by('-id')[:13]
    data = list(uploads.values())
    return JsonResponse(data, safe=False)

@csrf_exempt  # Only for development/testing; use CSRF tokens in production
def publish_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f'"topic" : "{data['topic']}" , "msg" : "{data['msg']}" ')

            # auth = {'username': settings.MQTT_USER, 'password': settings.MQTT_PASSWORD}
            # publish.single(f'{data['topic']}', f'{data['msg']}', hostname=settings.MQTT_SERVER, client_id="web_server", auth=auth)
            # return JsonResponse({'code': 0})

            # rc, mid = client.publish(f'{data['topic']}', f'{data['msg']}')
            # return JsonResponse({'code': rc})

            if not client.is_connected():
                print("client.reconnect()")
                mqttErrorCode = client.reconnect()
                if mqttErrorCode != 0:
                    return JsonResponse({'client.reconnect() MQTTErrorCode': mqttErrorCode})
            mqttMessageInfo = client.publish(f'{data['topic']}', f'{data['msg']}')
            mqttMessageInfo.wait_for_publish()
            return JsonResponse({'mqttMessageInfo.rc': mqttMessageInfo.rc})
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'only POST allowed'}, status=405)
