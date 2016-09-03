#!/bin/python2

from pwn import *
from itertools import permutations

def is_pal(s):
    for i in range(len(s) // 2):
        if s[i] != s[len(s) - i -1]:
            return False

    return True

def nxt(r):
    l = r.recvline_contains('Case')
    log.info('At %s case' % l.split('#')[1])
    l = r.recvline().split()[2:]
    log.info('Got %s' % str(l))
    r.recvuntil(' ')
    return l


with remote('ppc1.chal.ctf.westerns.tokyo', 31111) as r:
    r.progress('Solving chals')
    r.recvlines(10)
    for i in range(30):
        line = nxt(r)
        # just brute force all variants until it won't a palindrome
        for l in permutations(line):
            if is_pal(''.join(l)):
                break
        r.send(' '.join(l) + '\n')
    r.interactive()
