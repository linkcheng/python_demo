# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import create_app
from flask_script import Manager, Server
from log import configure_logging

configure_logging()
app = create_app('default')
manager = Manager(app)


manager.add_command("runserver", Server(host="0.0.0.0", port=8000))


def run():
    manager.run()


@app.route('/')
@app.route('/index')
def index():
    return 'It works!'


if __name__ == '__main__':
    run()
