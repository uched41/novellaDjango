from main.src.logger import logger
from main.src.config import my_config
from main.src.mqtt_client import my_mqtt
from main.src.response import my_responses
from main.src.imageConverter import my_imageConverter
from main.src.filemanager import my_filemanager
from ast import literal_eval
import os, math


def send_command(uid, command):
    topic = my_config.get("mqtt", "device_topic_base")
    topic = "{}/{}".format(topic, uid)

    my_mqtt.publish(topic, command)
    ans = my_responses.wait_reply(uid)
    if ans == None:
        raise Exception("No reply from " + uid)
    return ans


def send_image(uid, imgname):
        if imgname[0] == '/':
            imgname = imgname[1:]
            
        bin_name = my_imageConverter.convert_image(imgname)
        if bin_name == None:
            raise Exception ("file error")

        print("starting sending procedure")
        BUF_SIZE = 1024
        topic = "novella/devices/{}/{}/".format(uid, "image")
        print(topic)
        
        # to start we add 'start' to end of topic and send
        # device will read this topic end and act accordingly
        ntopic = topic + "start"
        fpath = os.path.join(my_filemanager.bin_dir, bin_name)
        no_lines = os.stat(fpath).st_size / BUF_SIZE
        no_lines = math.ceil(no_lines)


        bin_name = "/" + bin_name   # needed for SPIFFS filesystem
        print("Sending file: {}, to device: {}".format(bin_name, uid))
        ndata = { "filename": bin_name, "no_lines": no_lines}

        print("Sending start message")
        my_responses.set_false(uid)
        my_mqtt.publish(ntopic, str(ndata))
        if my_responses.wait_reply(uid) != "OK":     # wait for reply from device
            print("no reply from device")
            raise Exception("device error")

        atopic = topic + "mid"

        with open(fpath, 'rb') as myfile:
            content = myfile.read()
            print("Sending file content")
            for x in range(0, no_lines):
                temp = content[ (x*BUF_SIZE) : (x*BUF_SIZE+BUF_SIZE)]
                my_mqtt.publish(atopic, temp)
                if my_responses.wait_reply(uid) != "OK":     # wait for reply from device
                    print("no reply from device")
                    raise Exception("device error")
            
        ltopic = topic + "end"
        my_mqtt.publish(ltopic, "End")
        if my_responses.wait_reply(uid) != "OK":     # wait for reply from device
            print("no reply from device")
            raise Exception("device error")
        my_responses.set_false(uid)
        print("File send complete")
