from logging import Handler
from os import popen
from django.conf import settings
LOGGING_XMPP_CONFIG = settings.LOGGING_XMPP_CONFIG


class SENDXMPPHandler(Handler):
    def emit(self, record):
        try:
            message = self.format(record)

            shell_command = "echo '{}' | {} -u {} -j {} -p {} {} --tls-ca-path='/etc/ssl/certs'".format(
                message,
                LOGGING_XMPP_CONFIG['LOGGING_XMPP_COMMAND'],
                LOGGING_XMPP_CONFIG['LOGGING_XMPP_SENDER'],
                LOGGING_XMPP_CONFIG['LOGGING_XMPP_SERVER'],
                LOGGING_XMPP_CONFIG['LOGGING_XMPP_PASSWORD'],
                LOGGING_XMPP_CONFIG['LOGGING_XMPP_RECIPIENT']
            )
            if LOGGING_XMPP_CONFIG['LOGGING_XMPP_USE_TLS'] == '1':
                shell_command += ' -t'

            p = popen(shell_command, "w")
            status = p.close()
            if status:
                print("sendxmpp_handler exit status", status)

        except Exception:
            self.handleError(record)
