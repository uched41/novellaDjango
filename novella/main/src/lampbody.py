from novella.logger.logger import logger
from novella.database.database_client import my_database
from novella.config.config import my_config
from novella.device.mcu import Mcu

lampbody_columns = " (No INT AUTO_INCREMENT, device_id TEXT, current_pair TEXT, settings TEXT, misc TEXT, PRIMARY KEY (No) ) "


# Lampbody class which inherites for partne class Mcu
class Lampbody(Mcu):

    def __init__(self, **kwargs):
        # create table if it doesnt exist already
        if my_database.create_table(table="lampbodies", columns=lampbody_columns) is False:
            raise Exception("Unable to create table - lampbodies")

        self.device_id = kwargs["device_id"]
        self.group = "lampbodies"            # to be used by parent class to access Database Table

        # check if device already in database or not
        if not my_database.is_in_table(table="lampbodies", column="device_id", query=self.device_id):

            # create entry for new lampbody
            table = "lampbodies"
            template = " (device_id, settings) VALUES (%s, %s) "
            self.settings = my_config.get("lampbody", "default_settings")
            values = [self.device_id, str(self.settings)]

            if my_database.insert_in_table(table=table, template=template, value=values) is False:
                raise Exception("Unable to create lampbody object")

            Lampbody.debug("Created new lampbody object: " + self.device_id)

        else:       # is the device is already in our database
            Lampbody.debug("Device already in database: " + self.device_id)



    def __str__(self):
        return self.device_id


    @staticmethod
    def debug(*args):
        global logger
        logger.debug("Lampbody", *args)


    @staticmethod
    def error(*args):
        global logger
        logger.error("Lampshade", *args)


#my_lampbody = Lampbody(device_id="D48084332")
