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
# sock.send(b'(2, (700000, 0.06, 100, 63, 1))')
# Взрыв СП
# sock.send(b'(3, (254400, 46000, 0.1, 500))')
# sock.send(b'(4, (254400, 46000, 0.1))')
# sock.send(b'(5, (254400, 46000, 0.1))')
# TVS
# sock.send(b'(6, (1,1,2000,46000,7,2,60))')
# sock.send(b'(7, (1,1,100,46000,7,2))')
# sock.send(b'(8, (1,4,100,46000,7,2))')
# огненный шар
# sock.send(b'(9, (2000,450,100))')
# sock.send(b'(10, (2000,450))')
# sock.send(b'(11, (2000,450))')
# НКПР-вспышка
sock.send(b'(12, (200,100,63,1.8))')


res = recvall(sock)
# res = sock.recv(65000)
print(res.decode())
sock.close()
