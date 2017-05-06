import datetime
from logging import LOG_LEVELS


# TODO: better

class FileLogger(object):
    def __init__(self, file_path, verbose=True):
        self._file_path = file_path
        self._verbose = verbose

    def log(self, msg, who="", level=LOG_LEVELS["info"]):
        if not self._verbose:
            return
        if len(who) > 0:
            msg = "{} | {}".format(who, msg)
        time_msg = datetime.datetime.now().strftime("%y.%m.%d %H:%M:%S")
        msg = "{} | {} | {}".format(msg, level, time_msg)
        with open(self._file_path, "ab") as f:
            f.write("{}  {}  {}\n".format("*" * 3, msg, "*" * 3))

    def info(self, msg):
        self.log(msg, LOG_LEVELS["info"])

    def error(self, msg):
        self.log(msg, LOG_LEVELS["error"])

    def fatal(self, msg):
        self.log(msg, LOG_LEVELS["fatal"])
