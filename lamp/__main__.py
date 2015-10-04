#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tornado.ioloop import IOLoop
from tornado.options import define, options
from lamp import Lamp

import logging
log = logging.getLogger(__name__)

define('host', default=None, help='lamp server host')
define('port', default=None, help='lamp server port', type=int)


def draw(lamp):
    log.info('DRAW STATE: %s COLOR: %s', lamp.state, lamp.color)


if __name__ == '__main__':
    options.parse_command_line()
    host = options.host or raw_input("enter host (localhost): ") or 'localhost'
    port = options.port or int(raw_input("enter port (9999): ") or 9999)

    Lamp(host, port, on_change=draw).start()
    IOLoop.current().start()
