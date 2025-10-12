from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from django.http import HttpResponse, JsonResponse
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django_mqtt_mysql.mqtt_mysql import client
from myapp.models import Upload
from django.contrib.sessions.models import Session
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict

def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("/sessions/")
        else:
            device = request.user.device.device
            print(f"device {device}")
            return render(request, 'index.html', locals())
    else:
        return redirect("/login/")
    
@csrf_exempt  # Only for development/testing; use CSRF tokens in production
def login(request):
    if request.method=='POST':
        name = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=name, password=password)
        if user is not None:
            print("user is not None")
            if user.is_active:
                auth.login(request,user)
                message = "登入成功"
                return redirect('/') # *****
            else:
              message = "帳號尚未啟用!"  
        else:
            message = "登入失敗!"
        
        return render(request, 'login.html', locals())
    elif request.method=='GET':
        if request.user.is_authenticated:
            return redirect("/")
        else:
            return render(request, 'login.html', locals())
    
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect("/")
        return HttpResponse('logout')
    else:
        return redirect("/login/")


def upload_list(request):
    if request.user.is_authenticated:
        user = request.user
        device = user.device.device
        uploads =  Upload.objects.filter(device=device).order_by('-id')[:13]
        data = list(uploads.values())
        result = {}
        result['status'] = "success"
        result['data'] = data
        return JsonResponse(result)
    else:
        return JsonResponse({'status': 'Auth Fail'})

def upload_update(request, id):
    if request.user.is_authenticated:
        user = request.user
        device = user.device.device
        uploads = Upload.objects.filter(device=device, id__gt=id).order_by('-id')[:13]
        data = list(uploads.values())
        result = {}
        result['status'] = "success"
        result['data'] = data
        return JsonResponse(result)
    else:
        return JsonResponse({'status': 'Auth Fail'})

@csrf_exempt  # Only for development/testing; use CSRF tokens in production
def publish_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f'"topic" : "{data['topic'].strip()}" , "msg" : "{data['msg']}" ')

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
            mqttMessageInfo = client.publish(f'{data['topic'].strip()}', f'{data['msg']}')
            mqttMessageInfo.wait_for_publish()
            return JsonResponse({'mqttMessageInfo.rc': mqttMessageInfo.rc})
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'only POST allowed'}, status=405)
    
def sessions_list(request):
    if request.user.is_authenticated and request.user.is_superuser:
        sessions = Session.objects.all().order_by("-expire_date")
        current_key = request.session.session_key
        # 收集 user_id -> username
        user_ids = []
        decoded_map = {}
        for s in sessions:
            data = s.get_decoded()
            decoded_map[s.session_key] = data
            uid = data.get("_auth_user_id")
            if uid:
                user_ids.append(uid)

        usernames = {}
        if user_ids:
            User = get_user_model()
            users = User.objects.filter(id__in=set(map(int, user_ids)))
            usernames = {str(u.id): (u.get_username() or str(u)) for u in users}

        rows = []
        for s in sessions:
            data = decoded_map.get(s.session_key, {})
            rows.append({
                "session_key": s.session_key,
                "expire_date": s.expire_date,
                "last_seen": data.get("last_seen"),   # 需你有 middleware 寫入
                "ua": data.get("ua"),                 # 需你在登入時寫入
                "ip": data.get("ip"),                 # 需你在登入時寫入
                "username": usernames.get(data.get("_auth_user_id")),
            })

        return render(request, "sessions_list.html", {"rows": rows,"current_key":current_key})
    else:
        return redirect("/login/")

@csrf_exempt  # Only for development/testing; use CSRF tokens in production
def sessions_logout(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method != "POST":
            return HttpResponse("POST only")
        key = request.POST.get("session_key")
        current_key = request.session.session_key
        if not key:
            return HttpResponse("Missing session_key")
        try:
            s = Session.objects.get(session_key=key)
        except Session.DoesNotExist:
            raise HttpResponse("Session 不存在")

        if current_key == key:
            auth.logout(request)
            return redirect('/login/')
        else:
            s.delete()
            return redirect('/sessions/')
    else:
        return redirect("/login/")

