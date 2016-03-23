#!/usr/bin/env python
#coding:utf-8

import sys

class _Getch:
    """
    Gets a single character from standard input.  
    Does not echo to the screen.
    """
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()
 
    def __call__(self): 
        return self.impl()
 
 
class _GetchUnix:
    def __init__(self):
        import tty, sys
 
    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd, termios.TCSANOW)
            ch = sys.stdin.read(1)
            sys.stdout.write(ch)  # console show input
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
 
 
class _GetchWindows:
    def __init__(self):
        import msvcrt
 
    def __call__(self):
        import msvcrt
        return msvcrt.getch()
 
 
getch = _Getch()


def rcvQuit():
    command = ""
    while True:
        ch = getch()
        if ch == "\r":
            print("\nExecute command: " + command)
            command = ""
            sys.stdout.write("\033[80D")
        else:
            command += ch
            if command == "quit":
                sys.stdout.write("\033[80D")
                print "\nBye."
                break
                

def rcvPswd():
    command = ""
    while True:
        ch = getch()
        if ch == "\r":
            print("password = " + command)
            break
        else:
            command += ch
             

if __name__ == '__main__':
    import getpass  
    password = getpass.getpass('Enter password: ')  
    print password  
    rcvPswd()
    
