# !/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask_script import Shell
from instance import app, manager, run


def make_shell_context():
    return dict(app=app)


manager.add_command("shell", Shell(make_context=make_shell_context))


if __name__ == '__main__':
    run()
