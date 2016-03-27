#YACST2

> Captcha is a modern simple Turing test for everyday use, for human
> it's simple, but for bot or a simple neural network captcha can become
> a hard nut to crack.
> 
> You can try to solve it with your AI too, but it definitely can be
> solved with several lines of code, isn’t it?
> 
> [link](http://yacst2.2016.volgactf.ru:8090/)
> 
> Hints
> 
> [gist](https://gist.github.com/volalex/799789663f8c29f1bb58)
> 
> [gist2](https://gist.github.com/volalex/4c62beaa721807dbc139) Adding a
> Noise

**Algorithm**

1. Send request to the site, get remaining number of captchas.
2. Download captcha using **curl** (don't ask me why!).
3. Send it to the *Google Speech Recognizer* using python module **speech_recognition**
4. Send numbers to the server.
5. Repeat until you receive flag.

[solve.py](./solve.py)

But last captcha I had to solve by myself.

Flag is:

> VolgaCTF{Sound IS L1ke M@th if A+B=C THEN C-B=A}
