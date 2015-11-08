#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 fumikazu.kiyota@gmail.com
#

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
import logging
import importlib
from lib import conf, loader


settings = conf.load()


def main(name):
    u"""サーバーの起動処理

    サーバーの設定の参照の方法

    :Example:

    >>> from server import settings

    """
    app = loader.app(name, settings)

    logging.warning('Starting %s app on %d port...' % (name, app['port']))

    server = HTTPServer(app['application'])
    server.bind(app['port'])
    server.start(app['worker_processes'])
    IOLoop.instance().current().start()

if __name__ == "__main__":
    try:
        define("app", default="main", help="app name", type=str)
        options.parse_command_line()
        main(options.app)
    except:
        importlib.import_module('lib.logger').sentry()
