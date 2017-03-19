import datetime


def log(msg, level=0, who=""):
    if len(who) > 0:
        msg = "{} | {}".format(who, msg)
    time_msg = datetime.datetime.now().strftime("%y.%m.%d %H:%M:%S")
    msg = "{} | {}".format(msg, time_msg)
    print "{}  {}  {}".format("*" * 3, msg, "*" * 3)
