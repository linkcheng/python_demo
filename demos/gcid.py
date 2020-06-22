#!/usr/bin/env python
# coding:utf-8  
# @Author: linkcheng
# function：get commit id and files' url

import os
import re
import sys
import subprocess
import getopt
import logging
import requests
import time
import HTMLParser
from gittle import Gittle
from multiprocessing import Process, Queue 
from functools import wraps


info_logger = logging.getLogger("info_log")

class Gcid():
    def __init__(self, name = '', pre_id = '-', now_id = '-', url = ''):
        self.__name = name
        self.__pre_id = pre_id
        self.__now_id = now_id
        self.__url = url
    
    def getName(self):
        return self.__name

    def getPreId(self):
        return self.__pre_id

    def getNowId(self):
        return self.__now_id
        
    def getUrl(self):
        return self.__url

    def setName(self, name):
        self.__name = name

    def setPreId(self, pre_id):
        self.__pre_id = pre_id

    def setNowId(self, now_id):
        self.__now_id = now_id
        
    def setUrl(self, url):
        self.__url = url

    def show(self):
        sys.stdout.write('|{0:<64}'.format(self.__name[-63:]))
        sys.stdout.write('|{0:<40}'.format(self.__pre_id))
        sys.stdout.write('|{0:<41}|\n'.format(self.__now_id))
        
    def showIncludeUrl(self):
        sys.stdout.write('%s\n' % self.__url)
        # sys.stdout.write('%s\n' % self.__name)
        sys.stdout.write('(<%s>→' % self.__pre_id)
        sys.stdout.write('<%s>)\n' % self.__now_id)


def usage():
    '''
    the usage of the gcid.
    '''
    sys.stdout.write('''Usage: gcid [-h] [--help]
            [-c commit_id]
            [-d directory]
            [-f file_name]
            [-u user_name]
            [-string password ]
            [--config=/etc/gcid.conf ]
            note: -u and -string or --config must be use with -c
        \n''')


def printInfo(path, pre, now):
    sys.stdout.write('|{0:<64}'.format(path))
    sys.stdout.write('|{0:<40}'.format(pre))
    sys.stdout.write('|{0:<41}|\n'.format(now))


def printWarn(files_count):
    if files_count > 200:
        s = 'There are too many tracked files (' + files_count + '). Are you sure to continue:(n/y)'
        ip = input(s).strip()[0]
        if 'y' != ip:
            sys.exit(0)

# from functools import wraps
def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        start = time.time()
        result = function(*args, **kwargs)
        end = time.time()
        
        info_logger.debug('Total time running %s: %s seconds' % (function.func_name, str(end-start)))
        return result
        
    return function_timer


def loggerConf(info_logger, log_lvl = logging.DEBUG):
    '''
    logging module config.
    '''
    info_format = '%(asctime)s - %(filename)s - [line:%(lineno)d] - %(levelname)s - %(message)s'
    info_logName = '/tmp/gcid.log'
    info_formatter = logging.Formatter(info_format)
    
    info_logger.setLevel(log_lvl)

    info_handler = logging.StreamHandler()
    info_handler.setLevel(logging.INFO)

    debug_handler = logging.FileHandler(info_logName, 'a')
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(info_formatter)
     
    info_logger.addHandler(info_handler)
    info_logger.addHandler(debug_handler )
    

def getRepo(path):
    '''
    get local repo.
    '''
    from dulwich.errors import NotGitRepository

    repo = None
    try:
        repo = Gittle(path)
    except NotGitRepository as e:
        info_logger.info(e)
    
    return repo


@fn_timer
def getIds(file_name):
    '''
    get file's commit lastest id by the file name.
    '''
    cmd = 'git log -2 "' + file_name + '" | grep commit'
    info_logger.debug('cmd = %s' % cmd)
    ids = ['-', '-']

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    for e in p.stderr:
        return ids

    for index, out in enumerate(p.stdout):
        if re.match(r'^commit ', out):
            ids[index] = re.split(r'commit ', out)[1][:-1]

    return ids


@fn_timer
def getFiles(queue, commit_id):
    '''
    get file by commit id.
    '''
    
    cmd = 'git show "' + commit_id + '" | grep "diff --git"'
    info_logger.debug('cmd = %s' % cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()
    
    files = []
    for f in p.stdout:   
        if re.match(r'diff --git', f):
            info_logger.debug('f = %s' % f)
            # diff --git a/Navi/Design/BasicDesign/Route/JA212&JA224&JA224AA L1.5_Route_BDS_(RouteDestSort).asta \
            # b/Navi/Design/BasicDesign/Route/JA212&JA224&JA224AA L1.5_Route_BDS_(RouteDestSort).asta\n
            if re.search(r'"', f):
                files.append(re.split(r'"', f)[1][2:])
            else:
                info_logger.debug(re.split(r' b', f))
                # if ['diff --git a/Navi/Design/BasicDesign/Route/JA212&JA224&JA224AA L1.5_Route_BDS_(RouteDestSort).asta', \
                # '/Navi/Design/BasicDesign/Route/JA212&JA224&JA224AA L1.5_Route_BDS_(RouteDestSort).asta\n']
                # then split first and last char
                files.append(re.split(r' b', f)[1][1:-1])
                
    queue.put(files)
    
    
@fn_timer
def getGcids(files):
    '''
    get Gcid by the files' name, it's a list.
    '''
    gcids = []
    for i, f in enumerate(files):
        info_logger.debug('file name = %s' % f)
        gcid = Gcid(f)
        ids = getIds(f)
        
        gcid.setNowId(ids[0])
        gcid.setPreId(ids[1])
        
        gcids.append(gcid)
     
    return gcids


@fn_timer
def getConfInfo(path):
    '''
    get username and password by the conf file.
    '''
    if not os.path.isfile(path):
        info_logger.info('%s is not exist!\n' % path)
        sys.exit(1)
        
    with open(path, 'r') as fp:
        # file format is 
        # username=******
        # password=******
        username = fp.readline().split('=')[1].strip(' \n')
        password = fp.readline().split('=')[1].strip(' ')[:-1]
        info_logger.debug('username = %s' % username)
    
    return username, password
    

@fn_timer
def getCookie(queue, session, username, password):
    '''
    get cookie for geturl by username, password.
    '''
    start = time.time()
    url = 'http://igerrit/login/#/q/status:open'
    data = {
        'username':username,
        'password':password
    }
    
    response = session.post(url, data = data)
    
    if None == response.request.headers.get('Cookie'):
        queue.put(None)
        sys.exit(1)
    
    queue.put(response.request.headers.get('Cookie'))


@fn_timer
def getUrl(gcids, session, commit_id, cookie):
    '''
    get url for Gcids by commit_id, cookie.
    '''

    url = 'http://igerrit/gitweb?string=Doc/17Model/17Cy/21_UI.git;a=commit;h=' + commit_id
    headers = {'Cookie':cookie}
    
    response = session.request('GET', url, headers = headers)
    time_resp = response.elapsed.microseconds
    info_logger.debug("time_resp = %s" % str(time_resp/1000000.0))
    
    it = re.findall(r'<td><a class="list" href=.+?</a></td>', response.text)
    
    for i in it:
        s = re.findall(r'gitweb.+?;h=|Navi.+?</a>', i)
        url = 'http://igerrit/' + s[0][:-3]
        url_name = s[1][:-4]
        
        html_parser = HTMLParser.HTMLParser() 
        name = html_parser.unescape(url_name) 
        short_name = re.split(r'/', name)[-1]
        
        for g in gcids:
            if name == g.getName():
                g.setName(short_name)
                g.setUrl(url)
                g.showIncludeUrl()
                break

@fn_timer
def createGcids(files):
    '''
    create Gcid for every file and show the info.
    '''
    for f in files:
        info_logger.debug('file name = %s' % f)
        gcid = Gcid(f)
        ids = getIds(f)
        
        gcid.setNowId(ids[0])
        gcid.setPreId(ids[1])

        gcid.show()


def getIdsByFile(f):
    '''
    get id for the file
    '''
    pass


@fn_timer
def getIdsByDir(repo, directory):
    '''
    get ids for every tracked file in the directory.
    '''
    path = os.getcwdu() + '/' + directory
    if not os.path.isdir(path):
        info_logger.info('"%s" is a invalid directory, must be use a valid directory!' % d)
        sys.exit(1)
    os.chdir(path)
    
    re_str = r'^' + directory + '/'
    files = []
    for f in list(repo.tracked_files):
        if re.match(re_str, f):
            files.append(re.split(re_str, f)[1])

    files_count = len(files)
    printWarn(files_count)
    printInfo('path', 'comid-pre', 'comid-now')
    createGcids(files)
    info_logger.info('tracked files count = %d' % len(files))


@fn_timer
def getIdsByCmid(commit_id, username = None, password = None):
    '''
    get ids for every tracked file in the directory.
    '''
    
    proc_queue = Queue()
    
    proc_files = Process(target=getFiles, args=(proc_queue, commit_id)) 
    proc_files.start()
   
    if username and password:
        session = requests.Session()
        
        proc_cookie = Process(target=getCookie, args=(proc_queue, session, username, password))  
        proc_cookie.start()
        proc_get = proc_queue.get()
        
        if type(proc_get) is list:
            files = proc_get
            cookie = proc_queue.get()
            if cookie == None:
                info_logger.info('username or password error!')
                sys.exit(1)
        else:
            cookie = proc_get
            files = proc_queue.get()
        
        gcids = getGcids(files)
        info_logger.debug(cookie)
        
        getUrl(gcids, session, commit_id, cookie)
        info_logger.info('tracked files count = %d' % len(files))
    else:
        printInfo('path', 'comid-pre', 'comid-now')
        files = proc_queue.get()
        createGcids(files)
        info_logger.info('tracked files count = %d' % len(files))
    

@fn_timer   
def getIdsInRepo(repo):
    '''
    get ids for every tracked file in the repo.
    '''
    files = list(repo.tracked_files)
    files_count = len(files)
    
    printWarn(files_count)
    printInfo('path', 'comid-pre', 'comid-now')
    
    createGcids(files)
    info_logger.info('tracked files count = %d' % len(files))


@fn_timer
def runMain(repo):
    '''
    main thread.control the swtich by options.
    '''
    try:  
        opts, args = getopt.getopt(sys.argv[1:], 'ahpc:d:f:u:', ['help', 'config='])
        options = dict(opts)
        
        if options.has_key('-string'):
            import getpass  
            password = getpass.getpass('Enter password: ')  
            # print('%r')
        if options.has_key('-h') or options.has_key('--help'):
            usage()
            sys.exit(1)
        elif options.has_key('-a'):
            getIdsInRepo(repo)
        elif options.has_key('-c'):
            if 6 > len(options['-c']):
                info_logger.info('The length of commit id must be more than 6!')
            else:
                if options.has_key('-u') and options.has_key('-string'):
                    getIdsByCmid(options['-c'], options['-u'], password)
                elif options.has_key('--config'):
                    uname, passwd = getConfInfo(options['--config'])
                    getIdsByCmid(options['-c'], uname, passwd)
                else:
                    getIdsByCmid(options['-c'])
        elif options.has_key('-d'):
            if '/' == options['-d'][-1]:
                options['-d'] = options['-d'][:-1]
            getIdsByDir(repo, options['-d'])
        elif options.has_key('-f'):
            getIdsByFile(options['-f'])
        else:
            getIdsInRepo(repo)
        
    except getopt.GetoptError as e:
        info_logger.info('get options error: %s ' % e)
        usage()
        sys.exit(1)


if "__main__" == __name__:
    path = os.getcwdu()
    
    repo = getRepo(path)
    if not repo:
        sys.exit(1)
    else:
        os.chdir(path)

    loggerConf(info_logger)
    runMain(repo)
    info_logger.info('current path : %s\n' % path)
    
