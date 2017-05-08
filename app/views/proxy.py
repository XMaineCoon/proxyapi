#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author GinPonson
#
import random
from logging import getLogger

from flask import Blueprint, jsonify
from flask import request

from app.models.proxy import Proxy

proxy = Blueprint('proxy', __name__)


@proxy.route("/list/<int:page>", methods=["GET"])
def proxy_list(page):
    getLogger("proxyapi").info("request ip => %s" % request.remote_addr)
    proxy_list = Proxy.query.find_by_page(page)
    if len(proxy_list) == 0:
        return jsonify(code=404, codeMsg="no result")
    random.shuffle(proxy_list)
    return jsonify(proxy_list=[e.serialize() for e in proxy_list],
                   code=200, codeMsg="ok")
