import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 8888))
sock.send(b'(2, [1, 4, 4])')
res = sock.recv(64)
print(res.decode())
sock.close()
