#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 fumikazu.kiyota@gmail.com
#

from tornado.web import Application
from raven.contrib.tornado import AsyncSentryClient
import importlib
import yaml
import models
from tornado.options import options
import logging


def app(name, settings):
    u"""起動するアプリケーションをロードする
    """
    options.log_file_prefix = settings["logging_path"]
    logging.getLogger().setLevel(settings['logging_level'])

    models.load(settings['db'])

    with open(settings['server_apps_conf_path'], 'r') as f:
        app_conf = yaml.load(f)
        server = app_conf['common'][name]
        if settings['env'] in app_conf:
            server.update(app_conf[settings['env']][name])

    ui = {'ui_modules': {}, 'ui_methods': {}}
    for ui_name in ui.keys()
        for package in server[ui_name].keys():
            for name in server[ui_name][package].keys():
                x = server[ui][package]
                xx = importlib.import_module("lib.%s.%s" % (ui_name, package))
                ui[ui_name].update({
                    name: getattr(xx, x))
                })
    settings.update(ui)

    routes = []
    for package in server['handlers'].keys():
        for uri in server['handlers'][package].keys():
            name = server['handlers'][package][uri]
            handler = importlib.import_module("handlers.%s" % package)
            routes.append((r"%s" % uri, getattr(handler, name)))

    application = Application(routes, **settings)
    try:
        application.sentry_client = AsyncSentryClient(settings['sentry'])
    except:
        pass

    return dict(
        app = application, 
        port = server['port'],
        worker_processes = server['worker_processes']
    )
