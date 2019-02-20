from novella.logger.logger import logger
from novella.config.config import my_config
from novella.device.lampbody import Lampbody
from novella.device.lampshade import Lampshade
from novella.database.database_client import my_database
import novella.utils.utils as utils

lamp_columns = " (No INT AUTO_INCREMENT, name TEXT, lampbody_id TEXT, lampshade_id TEXT, settings TEXT, PRIMARY KEY (No) ) "


class Lamp:

    def __init__(self, **kwargs):
        if my_database.create_table(table="lamps", columns=lamp_columns) is False:
            raise Exception("Unable to create lamp table")

        # check if we already have this lamp in database
        if my_database.is_in_table(table="lamps", column="name", query=kwargs["name"]):
            Lamp.debug("Lamp already in Database")
            self.name = kwargs.get("name")
            temp = my_database.get_from_table(table="lamps", column="name", query=self.name, \
                    dcolumn=["lampshade_id", "lampbody_id"])
            temp = temp[0]
            shade_id = temp[0]
            body_id = temp[1]

            self.lampbody = Lampbody(device_id=body_id)
            self.lampshade = Lampshade(device_id=shade_id)
            return
        Lamp.debug("Making new Lamp.")

        # ensure that we have all necessary arguments
        if not my_database.in_list( ["name", "lampbody", "lampshade"], kwargs.keys() ):
            raise Exception("Incomplete args")

        Lamp.debug("Initializing Lamp")
        self.name = kwargs["name"]
        self.lampbody = kwargs["lampbody"]
        self.lampshade = kwargs["lampshade"]

        lampb = self.lampbody.device_id
        lamps = self.lampshade.device_id
        settings = my_config.get("lamp", "default_settings")

        template = " (name, lampbody_id, lampshade_id, settings) VALUES (%s, %s, %s, %s) "
        values = [self.name, lampb, lamps, str(settings)]

        if my_database.insert_in_table(table="lamps", template=template, value=values) is False:
            raise Exception("Unable to create new lamp object")

        Lamp.debug("Created new lamp")

        # set pairs
        Lamp.debug("Setting pairs")
        self.lampbody.set_pair(self.lampshade.device_id)
        self.lampshade.set_pair(self.lampbody.device_id)


    @staticmethod
    def debug(*args):
        global logger
        logger.debug("Lamp", *args)

    @staticmethod
    def error(*args):
        global logger
        logger.error("Lamp", *args)


