#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author GinPonson
#
import datetime

from flask_sqlalchemy import BaseQuery
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import VARCHAR

from app.extensions import db


class ProxyQuery(BaseQuery):
    def find_by_page(self, page):
        proxy_list = self.filter(Proxy.valid_times > 0).limit(page).all()
        return proxy_list


class Proxy(db.Model):
    __tablename__ = 't_proxy'

    query_class = ProxyQuery

    id = Column(Integer, primary_key=True, autoincrement=True)  # ID
    ip = Column(VARCHAR(16), nullable=False)  # IP
    port = Column(Integer, nullable=False)  # 端口
    level = Column(Integer, nullable=False, default=0)  # 匿名等级
    desc = Column(VARCHAR(100), nullable=False, default='')  # 描述
    protocol = Column(VARCHAR(100), nullable=False, default='')  # 协议
    country = Column(VARCHAR(100), nullable=False, default='')  # 国家
    area = Column(VARCHAR(100), nullable=False, default='')  # 地区
    crawl_time = Column(DateTime(), default=datetime.datetime.utcnow())  # 爬取时间
    speed = Column(Numeric(5, 2), nullable=False, default=0)  # 速度
    valid_times = Column(Integer, nullable=False, default=0)  # 检验次数
    update_time = Column(DateTime(), default=datetime.datetime.utcnow())  # 更新时间

    def serialize(self):
        return {
            'ip': self.ip,
            'port': self.port,
            'level': self.level,
            'desc': self.desc,
            'protocol': self.protocol,
            'country': self.country,
            'area': self.area,
            'speed': self.speed,
            'update_time': self.update_time.strftime("%Y-%m-%d %H:%M:%S")
        }
