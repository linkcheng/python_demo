#!/usr/bin python
import re

def comMat(str1):
    '''
    comMat
    '''
    pa = re.compile(r'({\[[\w]\]})')
    ma = pa.match(str1)
    print 'comMat rets = ', 
    print ma.groups()

def reMat(str1):
    '''
    reMat
    '''
    ma = re.match(r'[_a-zA-Z]+[_\w]*', str1)
    print 'reMat ret = %s' % ma.group()

def emailMat(str1):
    '''
    emailMat
    '''
    ma = re.match(r'^[\w]{6,20}@163.com$', str1)
    print 'emailMat ret = %s' % ma.group()

def xmlMat(str1):
    '''
    xmlMat
    '''
    ma = re.match(r'<([\w]+>)<([a-z]+>)[\w]+</\2</\1', str1)
    print 'xmlMat ret = %s' % ma.group()

def strSearch(str1):
    '''
    search
    '''
    ma = re.search(r'[\w]{6,20}@163.com', str1)
    print 'strSearch ret = %s' % ma.group()

def strFndAll(str1):
    '''
    findall
    '''
    ma = re.findall(r'\d+', str1)
    print 'strFndAll ret = %s' % ma

if __name__ == '__main__':
    comMat('{[h]}')
    reMat('He')
    emailMat('helloworld@163.com')
    xmlMat('<string><name>hello</name></string>')
    strSearch('asdfhf fdfsdjkfhasjkdhfadsdsfhafee@163.comadsfaedasf')
    strFndAll('a=90;b=80;c=100')
