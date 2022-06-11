import socketserver
import datetime
import math_test


class ThredingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class Safety_server(socketserver.BaseRequestHandler):

    def handle(self):
        bytes_in_handle = self.request.recv(1024).strip()

        addres = str(self.client_address[0])
        request = str(bytes_in_handle.decode())

        num_direction, data = self.get_data_in_request(request)

        if num_direction == 0:
            answer = 'error'
        elif num_direction == 1:
            answer = str(math_test.My_math().plus(data))
        elif num_direction == 2:
            answer = str(math_test.My_math().multiplication(data))
        else:
            answer = 'error'


        print(f'Adress: {addres}')
        print(f'Data: {request}')
        b = bytes(str(answer), encoding='utf-8')
        self.request.sendall(b)

        self.log_write(addres, request, answer)

    def log_write(self, addres: str, request: str, answer: str):
        """
        Функция записи обращений к серверу. Записывает ip-адрес,
        данные запроса, ответ сервера и дату(время) записи.
        @param addres: ip-адрес который обращается к серверу
        @param request: данные которые передал пользователь
        @param answer: ответ сервера
        """
        with open("log.txt", 'a') as file:
            today = datetime.datetime.today()
            file.write("-" * 10 + '\n')
            file.write(addres + '\n')
            file.write(request + '\n')
            file.write(answer + '\n')
            file.write(today.strftime("%Y-%m-%d-%H.%M.%S") + '\n')
            file.write("-" * 10 + '\n')

    def get_data_in_request(self, request: str):
        try:
            num_direction, data = eval(request)
            return num_direction, data
        except:
            num_direction, data = 0, 'error'
            return num_direction, data


if __name__ == '__main__':
    with ThredingTCPServer(('', 8888), Safety_server) as server:
        server.serve_forever()
