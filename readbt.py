#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys, getopt
from bencode import bdecode

import logging
logging.basicConfig(level=logging.DEBUG)

class torrent(object):
    comment  = ''
    announce = ''
    announces= []
    cdate    = ''
    info     = dict()

    def __init__(self, tdict):
        self.comment  = tdict['comment']
        self.announce = tdict['announce']
        self.announces= tdict['announce-list']
        self.cdate    = tdict['creation date']
        self.info     = tdict['info']
    def __del__(self):
        pass
    def display(self):
        print 'comment: {}'.format(self.comment)
        print 'creation date: {}'.format(self.cdate)
        print 'announce: {}'.format(self.announce)
        print 'announces: {}'.format(self.announces)
    def get_info(self):
        logging.debug('the info keys: {}'.format(self.info.keys()))
        logging.debug('name: {}'.format(self.info['name']))
        logging.debug('length: {}'.format(self.info['length']))
        logging.debug('piece length: {}'.format(self.info['piece length']))
        ps = self.info['pieces']
        logging.debug('pieces length: {}'.format(len(ps)))
        ret = []
        step = 20
        for x in range(0, len(ps), step) :
            ret.append(ps[x:x+step])
        logging.debug('piece#1: {}'.format(ret[0].encode('hex')))
        logging.debug('peerid: -PU1-{}'.format(str(id(self))))

def readbtfile(f):
    with open(f) as _f:
        ret = bdecode(_f.read())
    return ret

def connect_tracker(bt):
    pass


if __name__ == '__main__':
    short_opts = 'f:'
    opts, args = getopt.getopt(sys.argv[1:], short_opts)
    btfile = ''
    for k, v in opts:
        if k == '-f':
            btfile = v

    if btfile != '':
        btdict = readbtfile(btfile)

    if btdict != None:
        bt = torrent(btdict)
        bt.display()
        bt.get_info()
