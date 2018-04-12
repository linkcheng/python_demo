# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask_script import Manager, Server
from log import configure_logging
from app.app import create_app
from register import db

configure_logging()
app = create_app('default')
manager = Manager(app)

manager.add_command("runserver", Server(host="0.0.0.0", port=8000))


@app.before_request
def connect_db():
    if db.is_closed():
        db.connect()


@app.teardown_request
def close_db(exc):
    if not db.is_closed():
        db.close()


@app.route('/')
@app.route('/index')
def index():
    return 'It works!'


def run():
    manager.run()


if __name__ == '__main__':
    run()
