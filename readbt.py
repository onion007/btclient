#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys, getopt
from bencode import bdecode, bencode

import logging
logging.basicConfig(level=logging.DEBUG)

import urllib, socket, struct, hashlib


def getHTML(url):
    resp = urllib.urlopen(url)
    benbuf = resp.read()
    if benbuf[0] == 'd' and benbuf[-1] == 'e':
        return bdecode(benbuf)
    else:
        return None

def send_data(data, host, port):
    """ Send handshake and return data """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print '{}:{}'.format(host,port)
    t = {'data': data}
    print 'data len:{}'.format(len(data))
    print 'data: {}'.format(t)
    s.connect((host, port))
    #s.connect(('10.86.3.211', 51413))
    s.send(data)
    ret = s.recv(len(data))

    #data2 = struct.pack('LB1334x',
    #        1335,
    #        0x5
    #        )
    data2 = struct.pack('LB',
            0x1,
            0x2)

    print 'send: {}'.format({'send':data+data2})
    s.send(data+data2)
    ret = s.recv(4096)

    s.close()
    return ret

class torrent(object):
    _comment  = ''
    _announce = ''
    _announces= []
    _cdate    = ''
    _info     = dict()
    _info_hash= ''

    _interval   = 0
    _complete   = ''
    _incomplete = ''
    _peers = [('10.86.3.211', 51413),]

    _peer_id = '-PU2006-000987654321'

    def __init__(self, tdict):
        self._comment  = tdict['comment']
        self._announce = tdict['announce']
        self._announces= tdict['announce-list']
        self._cdate    = tdict['creation date']
        self._info     = tdict['info']
        self._info_hash= hashlib.sha1(bencode(tdict['info'])).digest().encode('hex')
    def __del__(self):
        pass
    def display(self):
        print 'comment: {}'.format(self._comment)
        print 'creation date: {}'.format(self._cdate)
        print 'announce: {}'.format(self._announce)
        print 'announces: {}'.format(self._announces)
    def get_info(self):
        logging.debug('the info keys: {}'.format(self._info.keys()))
        logging.debug('name: {}'.format(self._info['name']))
        logging.debug('length: {}'.format(self._info['length']))
        logging.debug('piece length: {}'.format(self._info['piece length']))
    def announce(self):
        try:
            params = {
                    'info_hash': self._info_hash.decode('hex'),
                    'peer_id':  self._peer_id,
                    'port': 6881,
                    'left': 699400192,
                    'uploaded': 0,
                    'downloaded': 0,
                    'compact': 1
                    }
            url = self._announce + '?' + urllib.urlencode(params)
            logging.debug('connecting {} ...'.format(self._announce))
            data = getHTML(url)
            #print data
            self._interval = data.get('interval')
            self._complete = data.get('complete')
            self._incomplete = data.get('incomplete')
            peers = data.get('peers')
            for x in xrange(0, len(peers), 6):
                #print 'peer: {}.{}.{}.{}:{}'.format(*struct.unpack('4BH', peers[x:x+6]))
                #ip,port = struct.unpack('4BH', peers[x:x+6])
                ip = socket.inet_ntoa(peers[x:x+4])
                port = struct.unpack('H', peers[x+4:x+6])[0]
                #print 'peer: {}:{}'.format(ip,port)
                self._peers.append((ip, port))
            print self._peers
            #resp = urllib.urlopen(url)
            #bebuf = resp.read()
            #ret = bdecode(bebuf)
            #self._interval = ret.get('interval')
            #self._complete = ret.get('complete')
            #self._incomplete = ret.get('incomplete')
            #peers = ret.get('peers')
            #print 'peers information:'
            #print ret
        except:
            pass
    def generate_handshake(self):
        pstr = 'BitTorrent protocol'
        pstrlen = len(pstr)
        #reserved = '00000000'
        info_hash = self._info_hash.decode('hex')
        peer_id = self._peer_id
        #return pstrlen + pstr + reserved + info_hash + peer_id
        req = struct.pack('B19s8x20s20s',
                pstrlen,
                pstr,
                info_hash,
                peer_id
                )
        return req

    def send_handshake(self):
        hs = self.generate_handshake()
        peer = self._peers[0]
        logging.debug('data:{}'.format(hs))
        logging.debug('send data to {}'.format(peer))
        ret = send_data(hs, *peer)
        print 'len: {}'.format(len(ret))
        t = {'ret ': ret}
        print 'resp: {}'.format(t)

def readbtfile(f):
    with open(f) as _f:
        ret = bdecode(_f.read())
    return ret


if __name__ == '__main__':
    short_opts = 'f:'
    opts, args = getopt.getopt(sys.argv[1:], short_opts)
    btfile = ''
    btdict = None
    for k, v in opts:
        if k == '-f':
            btfile = v

    if btfile != '':
        btdict = readbtfile(btfile)

    if btdict != None:
        bt = torrent(btdict)
        bt.display()
        bt.get_info()
        #bt.announce()
        bt.send_handshake()
