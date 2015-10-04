# -*- coding: utf-8 -*-
from collections import defaultdict
from tornado import gen

import logging
log = logging.getLogger(__name__)


class Event(object):
    CONNECT = 'connect'
    CLOSE = 'close'
    DATA = 'data'
    ERROR = 'error'

    def __init__(self):
        self.__listeners = defaultdict(list)

    def on(self, name, callback):
        assert callable(callback)
        if callback in self.__listeners[name]:
            log.error('Duplicate listener!')
        else:
            self.__listeners[name].append(callback)

    @gen.coroutine
    def trigger(self, name, *args, **kwargs):
        for ev in self.__listeners[name]:
            yield gen.maybe_future(ev(*args, **kwargs))
