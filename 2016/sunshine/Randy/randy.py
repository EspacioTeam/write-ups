import socket
import time

HOST = '4.31.182.242'
PORT = 9002
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
time.sleep(1)
s = sock.recv(1024)
print(s)
num = ""
for i, c in enumerate(s[41:45]):
    num = "%02X" % ((c - 0x41) % 256) + num

b = bytes.fromhex(num)
print(b)
sock.sendall(b)
s = sock.recv(1024)
print(s)
sock.close()
