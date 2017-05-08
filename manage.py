#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author GinPonson
#
from flask_script import Manager
from flask_script import Server
from flask_script import Shell
from flask_script import prompt_bool

from app import create_app
from app.extensions import db

app = create_app('config.cfg')

manager = Manager(app)

manager.add_command("runserver", Server('0.0.0.0', port=8080))


def _make_context():
    return dict(db=db)


manager.add_command("shell", Shell(make_context=_make_context))


@manager.command
def createall():
    "Creates database tables"
    db.create_all()


@manager.command
def dropall():
    "Drops all database tables"

    if prompt_bool("Are you sure ? You will lose all your data !"):
        db.drop_all()


if __name__ == "__main__":
    manager.run()
