import time
from main.models import Lampshade, Lampbody, Lamp

# This class object will store the response from each device

class Response:
    def __init__(self):
        self.data = dict()
        self.online_timeout = 120   # seconds
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


    def set_online(self, device, type):
        if device not in self.data.keys():
            d = dict()
            d["new"] = False 
            self.data[device] = d
        self.data[device]["last_updated"] = time.time()
        self.data[device]["type"] = type


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


    def wait_reply(self, device, timeout=5):
        oldTime = time.time()
        print("Waiting for reply from: {}".format(device))
        while (time.time()-oldTime < (timeout) ):
            if self.data[device]["new"] is True:
                res = self.data[device]["response"]
                self.data[device]["new"] = False
                return res

        print("Timeout, NO response from {}".format(device))
        return None


# response instance
my_responses = Response()
