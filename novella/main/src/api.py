from novella.logger.logger import logger
from novella.config.config import my_config
from novella.device.lampbody import Lampbody
from novella.device.lampshade import Lampshade
from novella.device.lamp import Lamp
from novella.database.database_client import my_database
from novella.filemanager.filemanager import my_filemanager
from novella.mqtt.mqtt_client import my_mqtt
from novella.response.response import my_responses
from novella.image.imageConverter import my_imageConverter

import flask
from flask import request, jsonify

app = flask.Flask(__name__)
#app.config["DEBUG"] = True

class ApiLogger:
    @staticmethod
    def debug(*args):
        logger.debug("API", *args)

    @staticmethod
    def error(*args):
        logger.debug("API", *args)


# lamps endpoint
@app.route('/lamps', methods=['GET'])
def api_lamps():
    params = request.args

    command = params.get("command")     # Get command to be run
    ApiLogger.debug("received new command: " + str(params))

    ####
    # SEND IMAGE TO LAMP
    # args: command, lamp_name, image_name
    ###
    if command == "send_image":
        lampname = params.get("lamp_name")
        imgname = params.get("image_name")

        ans = "OK"
        try: 
            tlamp = Lamp(name=lampname)
            tlamp.lampshade.send_image(imgname)
        except Exception as e:
            ApiLogger.debug(e)
            ans = "Error"

        return jsonify(response=ans)


    ####
    # SEND COMMAND TO LAMP
    # args: command, lamp_name, device_type, lamp_command
    ###
    elif command == "send_command":
        lampname = params.get("lamp_name")
        type = params.get("device_type")
        lcommand = params.get("lamp_command")

        ans = None
        try:
            tlamp = Lamp(name=lampname)
            if type == "lampbody":
                ans = tlamp.lampbody.send_command(lcommand)
            elif type == "lampshade":
                ans = tlamp.lampshade.send_command(lcommand)
        except Exception as e:
            ApiLogger.debug(e)
            return jsonify(response="error")

        return jsonify(response = ans)

    ####
    # GET ONLINE DEVICES
    # args: command, device_type
    ###
    elif command == "get_online_devices":
        type = params.get("device_type")
        ans = my_responses.get_online_devices(type)
        return jsonify(response=ans)


    ####
    # GET ONLINE LAMPS
    # args: command
    ###
    elif command == "get_online_lamps":
        ans = my_responses.get_online_lamps()
        return jsonify(response=ans)


    ####
    # MAKE NEW LAMP
    # args: command, body_id, shade_id, lamp_name
    ###
    elif command == "make_lamp":
        body_id = params.get("body_id")
        shade_id = params.get("shade_id")
        lampname = params.get("lamp_name")

        try:
            body = Lampbody(device_id=body_id)
            shade = Lampshade(device_id=shade_id)
            lamp = Lamp(name=lampname, lampbody=body, lampshade=shade)
        except Exception as e:
            ApiLogger.debug(e)
            return jsonify(response="Error")
            
        return jsonify(response="True")

    return jsonify(response=None)



if __name__ == '__main__':
    app.run(host='0.0.0.0')
    ApiLogger.debug("Starting server")
