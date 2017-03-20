import datetime

LOG_LEVELS = {
    "info": "info",
    "error": "error",
    "fatal": "fatal"
}


class Logger(object):
    def __init__(self, who="", verbose=True):
        self._who = who
        self._verbose = verbose

    def log(self, msg, level=LOG_LEVELS["info"]):
        if not self._verbose:
            return
        # TODO: colored printing (termcolor?)
        if len(self._who) > 0:
            msg = "{} | {}".format(self._who, msg)
        time_msg = datetime.datetime.now().strftime("%y.%m.%d %H:%M:%S")
        msg = "{} | {} | {}".format(msg, level, time_msg)
        print "{}  {}  {}".format("*" * 3, msg, "*" * 3)
