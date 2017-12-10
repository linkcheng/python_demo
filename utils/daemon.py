#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import print_function
import os
import sys
import atexit
import signal
from functools import wraps
from settings import os_env


class Daemon(object):
    """
    守护进程
    通过添加 @Daemon 装饰器实现守护进程模式，默认是单例模式，即一次只能跑一个实例，可以通过修改 pidfile 实现跑不同的实例
    """
    def __init__(self, pidfile='/tmp/daemon.pid', stdin='/dev/null', stdout='/tmp/daemon_out.log', stderr='/tmp/daemon_err.log'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    # Signal handler for termination (required)
    @staticmethod
    def __sigterm_handler(signo, frame):
        raise SystemExit(1)

    def daemonize(self):
        if os.path.exists(self.pidfile):
            raise RuntimeError('Already running.')

        # First fork (detaches from parent)
        try:
            if os.fork() > 0:
                raise SystemExit(0)
        except OSError as e:
            raise RuntimeError('fork #1 faild: {0} ({1})\n'.format(e.errno, e.strerror))

        os.chdir('.')
        os.setsid()
        os.umask(0o22)

        # Second fork (relinquish session leadership)
        try:
            if os.fork() > 0:
                raise SystemExit(0)
        except OSError as e:
            raise RuntimeError('fork #2 faild: {0} ({1})\n'.format(e.errno, e.strerror))

        # Flush I/O buffers
        sys.stdout.flush()
        sys.stderr.flush()

        # Replace file descriptors for stdin, stdout, and stderr
        with open(self.stdin, 'rb', 0) as f:
            os.dup2(f.fileno(), sys.stdin.fileno())
        with open(self.stdout, 'ab', 0) as f:
            os.dup2(f.fileno(), sys.stdout.fileno())
        with open(self.stderr, 'ab', 0) as f:
            os.dup2(f.fileno(), sys.stderr.fileno())

        # Write the PID file
        with open(self.pidfile, 'w') as f:
            print(os.getpid(), file=f)

        # Arrange to have the PID file removed on exit/signal
        atexit.register(lambda: os.remove(self.pidfile))

        signal.signal(signal.SIGTERM, self.__sigterm_handler)

    def start(self):
        if os_env == 'debug':
            return
        try:
            self.daemonize()
        except RuntimeError as e:
            print(e, file=sys.stderr)
            raise SystemExit(1)

    def stop(self):
        if os_env == 'debug':
            return
        try:
            if os.path.exists(self.pidfile):
                with open(self.pidfile) as f:
                    os.kill(int(f.read()), signal.SIGTERM)
            else:
                sys.stderr.write('Not running.')
                raise SystemExit(1)
        except OSError as e:
            if 'No such process' in str(e) and os.path.exists(self.pidfile):
                os.remove(self.pidfile)

    def restart(self):
        self.stop()
        self.start()

    def __call__(self, run):
        """
        实现类装饰器
        :param run: 要转化的方法名
        :return:
        """
        @wraps(run)
        def _call(*args, **kw):
            self.start()
            ret = run(*args, **kw)
            self.stop()
            return ret
        return _call
