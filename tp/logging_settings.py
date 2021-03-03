from copy import deepcopy
from django.utils.log import DEFAULT_LOGGING


def init_logging_settings():
    logging_dict = deepcopy(DEFAULT_LOGGING)
    logging_dict['handlers']['send_xmpp'] = {
        "level": "ERROR",
        "class": "tp.sendxmpp_handler.SENDXMPPHandler"
    }
    logging_dict['loggers']['django']['handlers'].append("send_xmpp")
    return logging_dict
