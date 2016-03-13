By running binary we can see strange symbols at debug info and they actually change every launch
>./randy_noflag 
>Welcome to Randy's TinyPoker! DebugInfo: g�[
>We've dealt you your hand face down, please enter it:

Ok, let's dive into the binary. We can see that that string was changed its from:
>Welcome to Randy's TinyPoker! DebugInfo: AAAA

It adds to each byte of the string (at "AAAA") corresponding byte from received random string:
![Debug](./debug_fixes.png)
It's quite big piece of code, but actually its logic is as simple as this pseudocode:
```python
r = rand()
s = "Welcome to Randy's TinyPoker! DebugInfo: AAAA"
l = s.find('AAAA')

for i in range(5):
    a = r >> (24 - 8 * i)
    s[l+i] = (s[l+i] + a) % 256

```
So it's very easy to see that we can [produce](./randy.py) reverse function and receive our flag:
Ehm, I forgot to save, so we'll be glad to receive PR for fixing this line :)
