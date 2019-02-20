
class Logger:
    def __init__(self, **kwargs):
        if "loglevel" in kwargs.keys():
            self.loglevel = loglevel

    def debug(self, module, *args):
        # arg[0] = msg
        # arg[1] = loglevel
        print("{}: {}".format(module, args[0]))

    def error(self, module, *args):
        print("{} Error: {}".format(module, args[0]))


logger = Logger()   # intialize first instance
