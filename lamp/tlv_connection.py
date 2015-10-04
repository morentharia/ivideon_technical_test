# -*- coding: utf-8 -*-
from binascii import hexlify
from struct import unpack
from tornado import gen
from tornado.tcpclient import TCPClient
import logging
log = logging.getLogger(__name__)

from .event import Event


class TLVConnection(Event):
    @gen.coroutine
    def connect(self, host, port):
        self.host = host
        self.port = port

        client = TCPClient()
        try:
            self.stream = yield client.connect(self.host, self.port)
        except IOError as e:
            log.error("%s", repr(e))
            raise gen.Return((False, 'Failed to connect'))
        self.trigger(Event.CONNECT, self)
        raise gen.Return((True, "OK"))

    @gen.coroutine
    def read_command(self):
        try:
            res = yield self._read_command()
        except IOError as e:
            self.stream.close()
            yield self.trigger(Event.CLOSE, self, error=e)
            res = (False, str(e))
        except Exception as e:
            self.stream.close()
            yield self.trigger(Event.ERROR, self, error=e)
            res = (False, str(e))
        finally:
            raise gen.Return(res)

    @gen.coroutine
    def _read_command(self):
        data = yield self.stream.read_bytes(3)
        log.debug('read header [%s]', hexlify(data))
        ctype, clength = unpack('>BH', data)
        log.debug('read header ctype = %s  clength = %s',
                  hex(ctype), hex(clength))
        if not clength:
            yield self.trigger(Event.DATA, ctype, data)
        else:
            data = yield self.stream.read_bytes(clength)
            log.debug('read body   [%s]', hexlify(data))
            yield self.trigger(Event.DATA, ctype, data)

        raise gen.Return((True, data))

    def __str__(self):
        return "{} {}:{}".format(self.__class__.__name__,
                                 self.host, self.port)
