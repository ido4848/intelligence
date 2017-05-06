import datetime
import termcolor
from logging import LOG_LEVELS

LOG_LEVELS_COLORS = {
    "info": "info",
    "error": "error",
    "fatal": "fatal"
}


class Logger(object):
    def __init__(self, who="", verbose=True):
        self._who = who
        self._verbose = verbose

    def color_text_by_level(self, text, level):
        if level == LOG_LEVELS["info"]:
            return text

        if level == LOG_LEVELS["error"]:
            return termcolor.colored(text, 'red')

        if level == LOG_LEVELS["fatal"]:
            return termcolor.colored(text, 'red', attrs=['reverse', 'blink'])

    def log(self, msg, level=LOG_LEVELS["info"]):
        if not self._verbose:
            return
        # TODO: colored printing (termcolor?)
        if len(self._who) > 0:
            msg = "{} | {}".format(self._who, msg)
        time_msg = datetime.datetime.now().strftime("%y.%m.%d %H:%M:%S")
        msg = "{} | {} | {}".format(msg, level, time_msg)

        print self.color_text_by_level("{}  {}  {}".format("*" * 3, msg, "*" * 3), level)

