import time
from main.models import Lampshade, Lampbody, Lamp
from main.src.config import my_config


# This object will run commands sent from device to server
class DeviceCommand:
    def delete_lamp(self, uid):
        if Lampshade.objects.filter(uid=uid).exists():
            lshade = Lampshade.objects.get(uid=uid)
            lamp = Lamp.objects.get(lampshade=lshade)
            print("Deleting Lamp {}".format(lshade.name))
            lamp.delete()

    def get_settings(self, device, mtype):
        ret = None
        if mtype == "lampbody" and Lampbody.objects.filter(uid = device).exists():
            lbody = Lampbody.objects.get(uid = device)
            lshade = lbody.lampshade
            if lshade:
                print("Lampbody {} coming online".format(device))
                lamp = Lamp.objects.get(lampshade=lshade)
                data = lamp.settings("lampbody")

                topic = my_config.get("mqtt", "device_topic_base")
                topic = "{}/{}".format(topic, device)
                ret = {
                    "data" : data,
                    "topic" : topic  
                }

        elif mtype == "lampshade" and Lampshade.objects.filter(uid = device).exists():
            lshade = Lampshade.objects.get(uid = device)
            lbody = lshade.lampbody 
            if lbody:
                print("Lampshade {} coming online".format(device))
                lamp = Lamp.objects.get(lampshade=lshade)
                data = lamp.settings("lampshade")

                topic = my_config.get("mqtt", "device_topic_base")
                topic = "{}/{}".format(topic, device)
                ret = {
                    "data" : data,
                    "topic" : topic  
                }


        return ret 

device_shell = DeviceCommand()



# This class object will store the response from each device

class Response:
    def __init__(self):
        self.data = dict()
        self.online_timeout = 10    # seconds
    # self.data = {
    #           "D91980029":{
    #               "response":"OK",
    #               "type     : "lampbody",
    #               "new"     : True,
    #               "last_updated"  : 499,
    #               },
    #       }
    def set(self, type, device, response):       # set a response value
        if device not in self.data.keys():
            d = dict()
            self.data[device] = d

        self.data[device]["type"] = type
        self.data[device]["response"] = response
        self.data[device]["new"] = True
        self.data[device]["last_updated"] = time.time()


    def get(self, device, val):         # Get response value
        tdata = self.data.get(device)
        if tdata and val in tdata.keys():
            self.data[device]["new"] = False
            return self.data[device][val]
        return None


    def is_updated(self, device):
        ans = self.data.get(device)
        if ans:
            return ans.get("new")
        return False


    def set_online(self, device, mtype):
        ret = None
        if device not in self.data.keys():
            d = dict()
            d["new"] = False 
            self.data[device] = d

        self.data[device]["last_updated"] = time.time()
        self.data[device]["type"] = mtype
        return ret


    def set_offline(self, device):
        self.data[device]["last_updated"] = 0


    def is_online(self, device):
        dev = self.data.get(device)
        if time.time() - dev.get("last_updated") < (60*self.online_timeout):
            return True
        return False


    def get_online_devices(self, type):     # get devices of a particular type that are online
        ans = []
        for dev in self.data.keys():
            dev2 = self.data.get(dev)
            if dev2.get("type") == type:
                if ( time.time() - dev2.get("last_updated") < (self.online_timeout) ):   # check if we have not received ping in a long time
                    ans.append(dev)
        return ans


    def get_online_lamps(self):
        online_shades = self.get_online_devices("lampshade")
        all_lamps = Lamp.objects.all()
        tans = []
        
        for lamp in all_lamps:
            if lamp.lampshade is not None:
                if lamp.lampshade.uid in online_shades:
                    tans.append(lamp.name)

        return tans


    def wait_reply(self, device, timeout=10):
        oldTime = time.time()
        print("Waiting for reply from: {}".format(device))
        while (time.time()-oldTime < (timeout) ):
            if self.data[device]["new"] is True:
                res = self.data[device]["response"]
                self.data[device]["new"] = False
                return res

        print("Timeout, NO response from {}".format(device))
        return None


    def set_false(self, device):
        self.data[device]["new"] = False


# response instance
my_responses = Response()
