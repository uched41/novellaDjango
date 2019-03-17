import paho.mqtt.client as mqtt
import time
import threading
from main.src.response import my_responses, device_shell
from main.src.logger import logger
import ast

mqtt_connected = False


class Mqtt:

    def __init__(self, server="0.0.0.0", port=1883, base_topic="novella/devices"):

        self.__server = server
        self.__port  = port

        # The mqtt msg processing, will feature sub topics under under the base
        # topics which will have their own individual handles
        self.topic_base = base_topic
        self.connect()

    def connect(self):
        self.__mqtt_client = mqtt.Client()
        self.__mqtt_client.on_connect = Mqtt.on_connect
        self.__mqtt_client.on_message = Mqtt.on_message
        self.__mqtt_client.on_disconnect = Mqtt.on_disconnect

        res = None
        retries = 0
        while res!=0 and retries < 10:
            try:
                retries += 1
                res = self.__mqtt_client.connect(self.__server, self.__port, 60)
            except Exception as e:
                Mqtt.debug(e)
            time.sleep(2)

        if res is 0:
            self.start_daemon()     # start the mqtt loop


    def subscribe(self, topic):
        global mqtt_connected
        if mqtt_connected:
            self.__mqtt_client.subscribe(topic)
            return True
        else:
            return False


    def publish(self, topic, message):
        global mqtt_connected
        if mqtt_connected:
            self.__mqtt_client.publish(topic, message)
            return True
        else:
            return None


    def start_daemon(self):
        self.subscribe("novella/devices/ping")
        Mqtt.debug("Starting mqtt loop")
        self.__mqtt_client.loop_start()
        #self.my_thread = threading.Thread(target = self.__mqtt_client.loop_forever())
        #threads.append(self.my_thread)
        #self.my_thread.start()


    @staticmethod
    def on_connect(client, userdata, flags, rc):
        global mqtt_connected
        Mqtt.debug("Connected to host")
        mqtt_connected = True           # Flag to enable us know connection state

        #TODO: Make modular
        client.subscribe("novella/devices/#")

    @staticmethod
    def on_disconnect(client, userdata, flags, rc):
        global mqtt_connected
        Mqtt.debug("Disconnected from host")
        mqtt_connected = False


    @staticmethod
    def on_message(client, userdata, msg):
        topic = msg.topic
        topic_parts = topic.split('/')

        data = ast.literal_eval((msg.payload).decode())

        # check if this is a ping message and act accordingly
        if "ping" in topic_parts:
            uid = data.get("id")
            mtype = data.get("type")
            Mqtt.debug("ping from {} {}".format(mtype, uid))
            ret = my_responses.set_online(uid, mtype)
            if ret:
                print(str(ret["topic"]))
                print(str(ret["data"]))
                client.publish(ret["topic"], str(ret["data"]))


        elif "response" in topic_parts:
            uid = data.get("id")
            res = data.get("response")
            Mqtt.debug( "{}: {}".format(uid, res) )
            if "lampbody" in topic_parts:
                my_responses.set("lampbody", uid, res)
            if "lampshade" in topic_parts:
                my_responses.set("lampshade", uid, res)


        elif "command" in topic_parts:
            cmd = data.get("command")
            uid = data.get("id")

            if(cmd == "Reset"):
                device_shell.deleteLamp(uid)
                

    @staticmethod
    def debug(*args):
        logger.debug("MQTT", *args)



    @staticmethod
    def error(*args):
        global logger
        logger.error("MQTT", *args)



# mqtt object
my_mqtt = Mqtt()
