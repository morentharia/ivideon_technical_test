# -*- coding: utf-8 -*-
from tornado import gen
import logging
log = logging.getLogger(__name__)


from .event import Event
from .tlv_connection import TLVConnection


class LampConnection(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.tlv_connection = TLVConnection()
        self.tlv_connection.on(Event.CONNECT, self.on_connect)
        self.tlv_connection.on(Event.DATA, self.on_data)
        self.tlv_connection.on(Event.CLOSE, self.on_close)
        super(LampConnection, self).__init__()

    @gen.coroutine
    def start(self):
        while True:
            attempt = 0
            while True:
                log.info("connecting %s:%s", self.host, self.port)
                is_ok, error_msg = yield self.tlv_connection.connect(self.host,
                                                                     self.port)
                if is_ok:
                    break
                else:
                    log.error(error_msg)
                    attempt += 1
                    yield self._wait_before_reconnect(attempt)
                    continue

            while True:
                is_ok, _ = yield self.tlv_connection.read_command()
                if not is_ok:
                    yield self._wait_before_reconnect(attempt=1)
                    break

    @gen.coroutine
    def _wait_before_reconnect(self, attempt):
        sec = 2 ** attempt
        if sec > 60:
            sec = 60
        log.info('sleep %s sec' % sec)
        yield gen.sleep(sec)

    @gen.coroutine
    def on_connect(self, tlv_connection):
        log.info("connected %s", tlv_connection)

    @gen.coroutine
    def on_close(self, tlv_connection, error):
        log.error("%s %s!!!!!", tlv_connection, type(error))

    @gen.coroutine
    def on_data(*argv, **kwargs):
        raise NotImplementedError
