from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from main.models import Lampbody, Lampshade, Lamp 
from main.src.imageConverter import my_imageConverter
from main.src.filemanager import my_filemanager
#from main.src.mqtt_client import my_mqtt
from main.src.response import my_responses
from main.src.hardwareFunctions import send_command, send_image
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def index(request):
    return render(request, 'main/main.html')


@csrf_exempt
def command(request):
    command = request.POST['command']

    response = dict()
    response["status"] = "Error"
    print(request)

    if command == "send_image":
        return sendImage(request)

    elif command == 'send_command':
        return sendCommand(request)

    elif command == 'get_online_lampbodies':
        return getOnlineLampbodies(request)

    elif command == 'get_online_lampshades':
        return getOnlineLampshades(request)

    elif command == "get_online_lamps":
        return getOnlineLamps(request)

    elif command == "make_lamp":
        return makeLamp(request)

    elif command == "get_lamp_details":
        return getLampDetails(request)

    else:
        return JsonResponse(response)


def sendCommand(request):
    lampname = request.POST["lamp_name"]
    type = request.POST["device_type"]
    lcommand = request.POST["lamp_command"]
    response = dict()
    response.status = ""

    try:
        lamp = Lamp.objects.get(name=lampname)
        if type == "lampbody":
            send_command(lamp.lampshade.lampbody.uid, lcommand)

        if type == "lampshade":
            send_command(lamp.lampshade.uid, lcommand)
    except Exception as e:
        response.status = "Error"
    else:
        response.status = "OK"

    return JsonResponse(response)


def sendImage(request):
    lampname = request.POST["lamp_name"]
    imgname = request.POST["image_name"]
    response = dict()
    response["status"] = ""

    try:
        lamp = Lamp.objects.get(name=lampname)
        send_image(lamp.lampshade.uid, imgname)
    except Exception as e:
        response["status"] = "Error"
    else:
        response["status"] = "OK"

    return JsonResponse(response)


def getOnlineLampbodies(request):
    response = dict()
    ans = my_responses.get_online_devices("lampbody")
    response["data"] = ans 
    return JsonResponse(response)


def getOnlineLampshades(request):
    response = dict()
    ans = my_responses.get_online_devices("lampshade")
    response["data"] = ans 
    return JsonResponse(response)


def getOnlineLamps(request):
    response = dict()
    ans = my_responses.get_online_lamps()
    response["data"] = ans 
    return JsonResponse(response)


def makeLamp(request):
    response = dict()
    body_id = request.POST["body_id"]
    shade_id = request.POST["shade_id"]
    lampname = request.POST["lamp_name"]

    if Lamp.objects.filter(name=lampname).exists():
        response["msg"] = "Lampname already exists, failed"
        return JsonResponse(response)

    # check if shade already belongs to another lamp
    lamps = Lamp.objects.all()
    for l in lamps:
        if l.lampshade.uid == shade_id:
            response["msg"] = "Error, Lampshade already belongs to another lamp"
            return JsonResponse(response)

        if l.lampshade.lampbody.uid == body.id:
            response["msg"] = "Error, Lampbody already belongs to another lamp"
            return JsonResponse(response)


    try:
        lampbody = Lampbody.objects.create(
            uid = body_id
        )

        lampshade = Lampshade.objects.create(
            uid = shade_id,
            lampbody = lampbody
        )

        lamp = Lamp.objects.create(
            name=lampname,
            lampshade=lampshade
        )
    except Exception as e:
        print(e)
        response["status"] = "Error"
        response["msg"] = "Unable to create lamp, error occured"
    else:
        response["status"] = "OK"
        response["msg"] = "Lamp created successfully"

    return JsonResponse(response)


def getLampDetails(request):
    response = dict()
    lampname = request.POST["lamp_name"]

    lamp = Lamp.objects.get(name=lampname)

    response["lampbody"] = lamp.lampshade.lampbody.uid 
    response["lampshade"] = lamp.lampshade.uid

    print(response)
    return JsonResponse(response)