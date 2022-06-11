import socketserver
import datetime
from calc.calc_strait_fire import Strait_fire


class ThredingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class Safety_server(socketserver.BaseRequestHandler):
    """
    Класс многопоточного сервера для получения данных от клиента
    и обработки информации
    """

    def handle(self):
        # 1. Получим информацию в байтах от клиента
        bytes_in_handle = self.request.recv(1024).strip()

        # 2. Определим ip-адрес и информацию от клиента
        addres = str(self.client_address[0])
        request = str(bytes_in_handle.decode())

        # 3. Попоробем взять № пути обработки и данные
        num_direction, data = self.get_data_in_request(request)

        # 4. По номеру пути определим, то что нужно клиенту:
        #       Коды:
        #           Пожар пролива
        #           0 - пожар пролива расстояние от геом.центра до облучаемого объекта
        #           1 - пожар пролива данные в каждой точке в виде кортежа (рассатояние, интенсивность, пробит, вероятность)
        #           2 - пожар пролива расстояние для интенсивностей (10.5, 7.0, 4.2, 1.4)
        #           ы
        #           ы

        if num_direction == 0:
            answer = Strait_fire().termal_radiation_point(S_spill=data[0], m_sg=data[1], mol_mass=data[2],
                                                          t_boiling=data[3], wind_velocity=data[4], radius=data[5])
        elif num_direction == 1:
            answer = Strait_fire().termal_radiation_array(S_spill=data[0], m_sg=data[1], mol_mass=data[2],
                                                          t_boiling=data[3], wind_velocity=data[4])
        elif num_direction == 2:
            answer = Strait_fire().termal_class_zone(S_spill=data[0], m_sg=data[1], mol_mass=data[2],
                                                     t_boiling=data[3], wind_velocity=data[4])
        else:
            answer = 'error'

        # 5. Закодируем ответ в байты и отправим его пользователю
        ans = bytes(str(answer), encoding='utf-8')
        self.request.sendall(ans)

        # 6. Запишем лог
        self.log_write(addres, request, str(answer))

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
