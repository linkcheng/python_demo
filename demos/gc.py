#!/usr/bin/env python
# coding=utf-8

from gittle import Gittle
import subprocess
import os
import re
import sys
import getopt


class Gcid():
    def __init__(self, name = '', pre_id = '-', now_id = '-'):
        self.__name = name
        self.__pre_id = pre_id
        self.__now_id = now_id
    
    def getName(self):
        return self.__name
 
    def getPreId(self):
        return self.__pre_id

    def getNowId(self):
        return self.__now_id

    def setName(self, name):
        self.__name = name

    def setPreId(self, pre_id):
        self.__pre_id = pre_id

    def setNowId(self, now_id):
        self.__now_id = now_id

    def show(self):
        print '|{0:<64}'.format(self.__name[-63:]),
        print '|{0:<40}'.format(self.__pre_id),
        print '|{0:<41}|\n'.format(self.__now_id)


def usage():  
    print '''Usage: gcid [-h] [--help]
            [-c commit_id]
            [-d directory]
            [-f file_name]'''


def printInfo(path, pre, now):
    print '|{0:<64}'.format(path),
    print '|{0:<40}'.format(pre),
    print '|{0:<41}|\n'.format(now)


def printWarn(files_count):
    if files_count > 200:
        s = 'There are too many tracked files (' + files_count + '). Are you sure to continue:(n/y)'
        ip = raw_input(s).strip()[0]
        if 'y' != ip:
            sys.exit(0)


def getRepo(path):
    from dulwich.errors import NotGitRepository

    repo = None
    try:
        repo = Gittle(path)
    except NotGitRepository as e:
        print e
    
    return repo


def getIds(f):
    cmd = 'git log -2 "' + f + '" | grep commit'
    # print 'CMD = %s' % cmd
    ids = ['-', '-']
    pos = 0

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    for e in p.stderr:
        p.wait()
        return ids

    for i in p.stdout:
        if re.match(r'^commit ', i):
            ids.insert(pos, re.split(r'commit ', i)[1][:-1])
            pos += 1
    p.wait()

    return ids


def createGcids(files):
    for f in files:
        print 'file name = %s' % f
        gcid = Gcid(f)
        ids = getIds(f)
        
        gcid.setNowId(ids[0])
        gcid.setPreId(ids[1])

        gcid.show()


def getIdsByFile(f):
    pass


def getIdsByDir(repo, d):
    path = os.getcwdu() + '/' + d
    if not os.path.isdir(path):
        print '"%s" is a invalid directory, must be use a valid directory!' % d
        sys.exit(1)
    os.chdir(path)
    
    r = r'^' + d + '/'
    files = []
    for f in list(repo.tracked_files):
        if re.match(r, f):
            files.append(re.split(r, f)[1])

    files_count = len(files)
    printWarn(files_count)
    printInfo('path', 'comid-pre', 'comid-now')
    createGcids(files)
    print '===================tracked files count = %d ===================' % len(files) 


def getIdsByCmid(c):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    cmd = 'git show "' + c + '" | grep "diff --git"'
    #print 'CMD = %s' % cmd
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
 
    files = []
    for f in p.stdout:  
        if re.match(r'diff --git', f):
        	print f
            if re.search(r'"', f):
                files.append(re.split(r'"', f)[1][2:])
            else:
                files.append(re.split(r' ', f)[2][2:])
    p.wait()

    printInfo('path', 'comid-pre', 'comid-now')
    createGcids(files)
    print '===================tracked files count = %d ===================' % len(files) 
    

def getIdsInRepo(repo):
    files = list(repo.tracked_files)
    files_count = len(files)
    printWarn(files_count)
    printInfo('path', 'comid-pre', 'comid-now')
    createGcids(files)
    print '===================tracked files count = %d ===================' % len(files) 


def runMain(repo):
    try:  
        opts, args = getopt.getopt(sys.argv[1:], 'ahc:d:f:', ['help', ])
        #print 'opts = %s' % opts
        #print 'args = %s' % args

        for opt, arg in opts:
            if opt in ('-h', '--help'):
                usage()
                sys.exit(1)
            elif '-a' == opt:
                getIdsInRepo(repo)
            elif '-c' == opt :
                if 6 > len(arg):
                    print 'The length of commit id must be more than 6!'
                else:
                    getIdsByCmid(arg)
            elif '-d' == opt:
                if '/' == arg[-1]:
                    arg = arg[:-1]
                getIdsByDir(repo, arg)
            elif '-f' == opt:
                getIdsByFile(arg)
            else:
                getIdsInRepo(repo)
            break
        else:
            getIdsInRepo(repo)

    except getopt.GetoptError as e:
        print 'get options error: %s ' % e
        usage()
        sys.exit(1)


if "__main__" == __name__:
    path = os.getcwdu()
    print '=================current path : %s =====================' % path

    repo = getRepo(path)
    if not repo:
        sys.exit(1)
    else:
        os.chdir(path)

    runMain(repo)