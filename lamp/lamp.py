# -*- coding: utf-8 -*-
from tornado import gen
from functools import partial

import logging
log = logging.getLogger(__name__)

from .lamp_connection import LampConnection


class Lamp(LampConnection):
    def __init__(self, host, port,
                 on_change=None, color='\x00\xDE\xAD', state='OFF'):
        self._color = color
        self._state = state

        if on_change:
            self.on_change = on_change
        else:
            def on_change(*argv, **kwargs):
                log.info('something changed')
            self.on_change = on_change

        super(Lamp, self).__init__(host, port)

    @gen.coroutine
    def on_data(self, ctype, data):
        func = getattr(self, 'command_%s' % hex(ctype),
                       partial(self.command_unknown, ctype))
        yield func(data)

    @gen.coroutine
    def command_0x12(self, data):
        """
            ON (включить фонарь): type = 0x12, length = 0
        """
        log.info('0x12 set state ON')
        self.state = 'ON'

    @gen.coroutine
    def command_0x13(self, data):
        """
            OFF (выключить фонарь): type = 0x13, length = 0
        """
        log.info('0x13 set state OFF')
        self.state = 'OFF'

    @gen.coroutine
    def command_0x20(self, data):
        """
            COLOR (сменить цвет): type = 0x20, length = 3,
            value интерпретируется как новый цвет фонаря в RGB.
        """
        log.info('0x20 color data %s', data)
        self.color = data

    @gen.coroutine
    def command_unknown(self, ctype, data):
        log.warn('Unknown command %s', hex(ctype))

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val):
        if self.state == val:
            return
        self._state = val
        self.on_change(self)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, val):
        if self._color == val:
            return
        self._color = val
        self.on_change(self)
