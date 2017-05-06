from intelligence.utilization.general_utilities.loggers.console_logger import ConsoleLogger


def apply_carefully(items, func, logger=ConsoleLogger(verbose=True)):
    products = []

    for item in items:
        try:
            products.append(func(item))
        except Exception as e:
            logger.log("Could not apply {} on {} with error {}".format(func, item, e))

    return products


DEFAULT_PREVIEW_LENGTH = 1000


def str_preview(str, max_len=DEFAULT_PREVIEW_LENGTH):
    if len(str) > max_len:
        char_len = (max_len - 5) / 2
        return "{} ... {}".format(str[0:char_len], str[len(str) - char_len:len(str)])
    else:
        return str
