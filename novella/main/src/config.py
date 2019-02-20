
class Default_Config:

    def __init__(self):
        self.data = {
            "database":{
                "host":"localhost",
                "user":"ched",
                "password":"uched4123",
                "database":"novella"
                },

            "lampbody":{
                "default_settings":{}
                },

            "lampshade":{
                "default_settings":{}
                },

            "lamp":{
                "default_settings":{}
                },

            "filemanager":{
                "parent_directory":"/code/.novella/",
                "image_directory":"images/",
                "bin_directory":"bin/"
                },

            "image":{
                "new_height":160,
                "new_width":90,
                },

            "mqtt":{
                "device_topic_base":"novella/devices",
                },
        }


    def get(self, *args):
        if len(args) == 0:
            return None

        ans = self.data
        for arg in args:
            if arg not in ans.keys():
                return None
            ans = ans[arg]

        return ans


    def set(self, *args, **kwargs):
        if len(args) == 0 or "value" not in kwargs.keys():
            return None
        # ToDo: Build out

# Config object
my_config = Default_Config()
