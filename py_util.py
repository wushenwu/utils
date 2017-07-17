# -*- coding: utf-8 -*-
import sys

def GetUTF8_Prefix(s):
    tmp = s.encode('utf-8').encode('hex')
    ret = ''
    for i in xrange(len(tmp) / 2):
        ret += '\\x'
        ret += tmp[i:i+2]
    return ret

def GetUTF8(s):
    return s.encode('utf-8').encode('hex')
    
def TestUnicode():
    print GetUTF8('install')
    print GetUTF8(u'退出')
    print GetUTF8(u'立即体验')