#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author GinPonson
#
import os
from logging import getLogger
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify
from flask import logging

from app.extensions import db
from app.views import proxy as views

DEFAULT_APP_NAME = 'proxyapi'

DEFAULT_BLUEPRINTS = (
    (views.proxy, "/proxy"),
)


def create_app(config=None, blueprints=None):
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(DEFAULT_APP_NAME)

    # config
    app.config.from_pyfile(config)

    configure_extensions(app)
    configure_logging(app)
    configure_errorhandlers(app)
    # register module
    configure_blueprint(app, blueprints)

    return app


def configure_extensions(app):
    # configure extensions
    db.init_app(app)


def configure_errorhandlers(app):
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify(error="Login required")

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify(error='Sorry, your request not allowed')

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify(error='Sorry, no such api')

    @app.errorhandler(500)
    def server_error(error):
        getLogger("app").exception(error)
        return jsonify(error='Sorry, an errors has occurred')


def configure_blueprint(app, blueprints):
    for blueprint, url_prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)


def configure_logging(app):
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')

    info_log = os.path.join(app.root_path,
                            app.config['INFO_LOG'])

    info_file_handler = \
        RotatingFileHandler(info_log,
                            maxBytes=100000,
                            backupCount=10)

    info_file_handler.setLevel(logging.DEBUG)
    info_file_handler.setFormatter(formatter)
    app.logger.addHandler(info_file_handler)

    error_log = os.path.join(app.root_path,
                             app.config['ERROR_LOG'])

    error_file_handler = \
        RotatingFileHandler(error_log,
                            maxBytes=100000,
                            backupCount=10)

    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    app.logger.addHandler(error_file_handler)
