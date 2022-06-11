import socket

def recvall(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            break
    return data


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 8888))
# Пожар пролива
# sock.send(b'(0, (200, 0.06, 100, 63, 1, 20))')
# sock.send(b'(1, (700000, 0.06, 100, 63, 1))')
sock.send(b'(2, (700000, 0.06, 100, 63, 1))')
res = recvall(sock)
# res = sock.recv(65000)
print(res.decode())
sock.close()
