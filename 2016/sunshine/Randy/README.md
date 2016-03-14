By running [binary](./randy_noflag) we can see strange symbols at debug info and they actually change every launch
>./randy_noflag 
>
>Welcome to Randy's TinyPoker! DebugInfo: g�[
>
>We've dealt you your hand face down, please enter it:

Ok, let's dive into the binary. We can see that the string changed its from:
>Welcome to Randy's TinyPoker! DebugInfo: AAAA

Code below adds to each byte of the substring "AAAA" corresponding byte from received random int:
![Debug](./debug_fixes.png)

It's quite big piece of code, but here we can see repeating blocks of opcodes. So logic can be rewrited in loop and it is as simple as this pseudocode:
```python
r = rand()
s = "Welcome to Randy's TinyPoker! DebugInfo: AAAA"
l = s.find('AAAA')

for i in range(5):
    a = r >> (24 - 8 * i)
    s[l+i] = (s[l+i] + a) % 256

```
Further we see such block:

![Branch](./branch.png)

So here we simple need to enter the value that equals to local_18h. If we look in first screenshot of code we see that it returned value of random function.

So it's very easy to see that we can [produce](./randy.py) reverse function for retrieving produced random value and receive our flag:

```python
def rev(x):
	ret=''
	for i in x:
		if ord(i)-0x41 < 0:
			ret+=chr(ord(i)-0x41+0xff+1)
		else:
			ret+=chr(ord(i)-0x41)
	return ret[::-1]

from pwn import *
#s=process('./randy_noflag')
s=remote('4.31.182.242',9002)
r=s.recv(100,timeout=1)
print r

s.sendline(rev(r[41:45]))
print s.recv(100,timeout=1)
```
