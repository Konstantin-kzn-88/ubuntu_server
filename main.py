import socketserver
from calc.calc_strait_fire import Strait_fire
from calc.calc_sp_explosion import Explosion
from calc.calc_tvs_explosion import Explosion as Explosion_tvs
from calc.calc_fireball import Fireball
from calc.calc_lower_concentration import LCLP
from calc.calc_liguid_evaporation import Liquid_evaporation


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
        #    Коды:
        #      Пожар пролива
        #      0 - пожар пролива расстояние от геом.центра до облучаемого объекта
        #      1 - пожар пролива данные в каждой точке в виде кортежа (рассатояние, интенсивность, пробит, вероятность)
        #      2 - пожар пролива расстояние для интенсивностей (10.5, 7.0, 4.2, 1.4)
        #      3 - взрыв (СП 12.13130-2009) для расстояния
        #      4 - взрыв (СП 12.13130-2009) данные в каждой точке в виде кортежа (рассатояние, давление, импульс, пробит, вероятность)
        #      5 - взрыв (СП 12.13130-2009) расстояние для давлений (100, 53, 28, 12, 5, 3)
        #      6 - взрыв (методика ТВС) для расстояния
        #      7 - взрыв (методика ТВС) данные в каждой точке в виде кортежа (рассатояние, давление, импульс, пробит, вероятность)
        #      8 - взрыв (методика ТВС) расстояние для давлений (100, 53, 28, 12, 5, 3)
        #      9 - огненный шар для расстояния
        #      10 - огненный шар данные в каждой точке в виде кортежа (рассатояние, интенсивность, доза, пробит, вероятность)
        #      11 - огненный шар расстояние для доз [600, 320, 220, 120] кДж/м2
        #      12 - НКПР и пожар-вспышка
        #      13 - Испарение ненагретой жидкости (для 3600 с)
        #      14 - Испарение ненагретой жидкости в каждой точке времени в виде кортежа (время, масса)

        # Пожар пролива
        if num_direction == 0:

            answer = Strait_fire().termal_radiation_point(S_spill=data[0], m_sg=data[1], mol_mass=data[2],
                                                          t_boiling=data[3], wind_velocity=data[4], radius=data[5])
        elif num_direction == 1:
            answer = Strait_fire().termal_radiation_array(S_spill=data[0], m_sg=data[1], mol_mass=data[2],
                                                          t_boiling=data[3], wind_velocity=data[4])
        elif num_direction == 2:
            answer = Strait_fire().termal_class_zone(S_spill=data[0], m_sg=data[1], mol_mass=data[2],
                                                     t_boiling=data[3], wind_velocity=data[4])
        # Взрыв СП
        elif num_direction == 3:
            answer = Explosion().explosion_point(mass=data[0], heat_of_combustion=data[1], z=data[2], radius=data[3])
        elif num_direction == 4:
            answer = Explosion().explosion_array(mass=data[0], heat_of_combustion=data[1], z=data[2])
        elif num_direction == 5:
            answer = Explosion().explosion_class_zone(mass=data[0], heat_of_combustion=data[1], z=data[2])

        # Взрыв ТВС
        elif num_direction == 6:
            answer = Explosion_tvs().explosion_point(class_substance=data[0], view_space=data[1], mass=data[2],
                                                     heat_of_combustion=data[3], sigma=data[4], energy_level=data[5],
                                                     radius=data[6])
        elif num_direction == 7:
            answer = Explosion_tvs().explosion_array(class_substance=data[0], view_space=data[1], mass=data[2],
                                                     heat_of_combustion=data[3], sigma=data[4], energy_level=data[5])
        elif num_direction == 8:
            answer = Explosion_tvs().explosion_class_zone(class_substance=data[0], view_space=data[1], mass=data[2],
                                                          heat_of_combustion=data[3], sigma=data[4],
                                                          energy_level=data[5])

        # Огненный шар
        elif num_direction == 9:
            answer = Fireball().fireball_point(mass=data[0], ef=data[1], radius=data[2])
        elif num_direction == 10:
            answer = Fireball().fireball_array(mass=data[0], ef=data[1])
        elif num_direction == 11:
            answer = Fireball().termal_class_zone(mass=data[0], ef=data[1])
        # Пожар вспышка
        elif num_direction == 12:
            answer = LCLP().lower_concentration_limit(mass=data[0], mol_mass=data[1], t_boiling=data[2],
                                                      lower_concentration=data[3])
        # Испарение ненагретой жидкости
        elif num_direction == 13:
            answer = Liquid_evaporation().evaporation_in_moment(time = 3600, steam_pressure=data[0], molar_mass=data[1],
                                                            strait_area=data[2])
        elif num_direction == 14:
            answer = Liquid_evaporation().evaporation_array(steam_pressure=data[0], molar_mass=data[1],
                                                            strait_area=data[2])

        else:
            answer = 'error'

        # 5. Закодируем ответ в байты и отправим его пользователю
        ans = bytes(str(answer), encoding='utf-8')
        # self.request.sendall(ans)
        self.send_msg(self.request, ans)

    def get_data_in_request(self, request: str):
        try:
            num_direction, data = eval(request)
            data = [float(i) for i in data]
            return num_direction, data
        except:
            num_direction, data = 404, 'error'
            return num_direction, data

    def send_msg(self, sock, msg):
        sock.sendall(msg)


if __name__ == '__main__':
    with ThredingTCPServer(('', 8888), Safety_server) as server:
        server.serve_forever()
