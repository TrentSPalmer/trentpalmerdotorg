from django.test import TestCase
import logging
from tp.sendxmpp_handler import SENDXMPPHandler

logger = logging.getLogger(__name__)
xH = SENDXMPPHandler()
xH.setLevel(logging.ERROR)
logger.addHandler(xH)


class TestSendXMPPHandlerTestCase(TestCase):

    def test_sendxmpp_handler(self):
        logger.debug('test_sendxmpp_handler_debug_test')
        logger.info('test_sendxmpp_handler_info_test')
        logger.warning('test_sendxmpp_handler_warning_test')
        logger.error('test_sendxmpp_handler_error_test')
        logger.critical('test_sendxmpp_handler_critical_test')
