from novella.logger.logger import logger
from novella.database.database_client import my_database
from novella.config.config import my_config
from novella.mqtt.mqtt_client import my_mqtt
from novella.response.response import my_responses
from ast import literal_eval

lampbody_columns = " (No INT AUTO_INCREMENT, device_id TEXT, current_pair TEXT, settings TEXT,\
                      misc TEXT, PRIMARY KEY (NO) )"


class Mcu:

    def __init__(cls, **kwargs):
        if "device_id" not in kwargs.keys():
            raise ValueError

        self.device_id = kwargs["device_id"]


    def set_pair(self, pair):
        table = self.group
        scolumns = [ "current_pair" ]
        dcolumn = "device_id"
        dvalue = self.device_id
        value = [ pair ]

        ans = my_database.update_table(table=table, scolumns=scolumns, dcolumn=dcolumn, dvalue=dvalue, value=value)
        if ans is not False:
            return True
        else:
            return False


    def get_pair(self):
        table = self.group
        column = "device_id"
        query = self.device_id
        dcolumn = ["current_pair"]

        ans = my_database.get_from_table(table=table, column=column, query=query, dcolumn=dcolumn)
        if ans is not False:
            return ans[0][0]
        return None


    def send_command(self, command):
        topic = my_config.get("mqtt", "device_topic_base")
        topic = "{}/{}".format(topic, self.device_id)

        my_mqtt.publish(topic, command)
        ans = my_responses.wait_reply(self.device_id)
        if ans == None:
            raise Exception("No reply from " + self.device_id)
        return ans


    def get_setting(self, setting):
        table = self.group
        column = "device_id"
        query = self.device_id
        dcolumn = ["settings"]

        ans = my_database.get_from_table(table=table, column=column, query=query, dcolumn=dcolumn)
        if ans is False:
            return None

        ans = ans[0][0]
        ans = literal_eval(ans)

        if setting in ans.keys():
            return ans[setting]
        return None


    def set_setting(self, setting, value):
        table = self.group
        column = "device_id"
        query = self.device_id
        dcolumn = ["settings"]

        ans = my_database.get_from_table(table=table, column=column, query=query, dcolumn=dcolumn)
        if ans is False:
            return None

        ans = ans[0][0]
        ans = literal_eval(ans)
        ans[setting] = value

        ans = str(ans)
        ans = my_database.update_table(table=table, scolumns=dcolumn, dcolumn=column, dvalue=query, value=ans)
        if ans is not False:
            return True
        return False


    def __str__(self):
        return self.device_id


    @staticmethod
    def debug(*args):
        global logger
        logger.debug("Mcu", *args)


    @staticmethod
    def error(*args):
        global logger
        logger.error("Mcu", *args)
