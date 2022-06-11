import socketserver

import math_test


class ThredingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class Safety_server(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024).strip()

        addres = str(self.client_address[0])
        request = str(data.decode())
        answer = str('[1,2,3,4]')

        print(f'Adress: {addres}')
        print(f'Data: {request}')
        b = bytes('[1,2,3,4]', encoding='utf-8')
        self.request.sendall(b)
        self.log_write(addres, request, answer)

    def log_write(self, addres: str, request: str, answer: str):
        with open("log.txt", 'a') as file:
            file.write("-" * 10 + '\n')
            file.write(addres + '\n')
            file.write(request + '\n')
            file.write(answer + '\n')
            file.write("-" * 10 + '\n')


if __name__ == '__main__':
    with socketserver.TCPServer(('', 8888), Safety_server) as server:
        server.serve_forever()
