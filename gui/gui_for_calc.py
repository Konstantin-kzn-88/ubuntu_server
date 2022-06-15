# -----------------------------------------------------------
# Класс GUI для визуализации результатов расчета на сервере
#
# (C) 2022 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------
from PySide2 import QtWidgets, QtGui, QtCore
import sys
import os
from pathlib import Path
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import socket

IP = '127.0.0.1'


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Calc_gui(QtWidgets.QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__()
        self.main_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/calc.png')
        save_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/save.png')
        calc_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/comp.png')
        book_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '/ico/book.png')

        print(str(Path(os.getcwd()).parents[0]))
        # Главное окно
        self.setFixedSize(1300, 1200)
        self.setWindowTitle('Safety calc (v.1.0)')
        self.setWindowIcon(self.main_ico)

        central_widget = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout(self)
        grid.setColumnStretch(0, 2)
        grid.setColumnStretch(1, 6)

        # 1.Окно ввода данных
        self.table_data = QtWidgets.QTableWidget(0, 2)
        self.table_data_view()  # фукция отрисовки заголовков таблицы
        # 2. Окно текстового результата и выбранная методика
        self.result_text = QtWidgets.QPlainTextEdit()
        self.selected_method = QtWidgets.QLabel()
        self.selected_method.setText('Пожар пролива')
        self.set_param_names_in_table()
        # Упакуем 1 и 2 в vbox
        layout_data = QtWidgets.QFormLayout(self)
        GB_data = QtWidgets.QGroupBox('Ввод данных и результат')
        GB_data.setStyleSheet("QGroupBox { font-weight : bold; }")
        vbox_data = QtWidgets.QVBoxLayout()
        vbox_data.addWidget(self.table_data)
        vbox_data.addWidget(self.result_text)
        vbox_data.addWidget(self.selected_method)
        layout_data.addRow("", vbox_data)
        GB_data.setLayout(layout_data)
        # 3.График
        sc = MplCanvas(self, width=5, height=13, dpi=100)
        sc.axes.plot([0, ], [0, ])

        layout_graph = QtWidgets.QFormLayout(self)
        GB_graph = QtWidgets.QGroupBox('Графическое отображение')
        GB_graph.setStyleSheet("QGroupBox { font-weight : bold; }")
        layout_graph.addRow("", sc)
        GB_graph.setLayout(layout_graph)

        grid.addWidget(GB_data, 0, 0, 1, 1)
        grid.addWidget(GB_graph, 0, 1, 0, 1)
        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)

        # Меню приложения (верхняя плашка)
        # 1. file_menu
        # 1.1. Расчет
        calc_menu = QtWidgets.QAction(calc_ico, 'Расчет', self)
        calc_menu.setShortcut('Ctrl+D')
        calc_menu.setStatusTip('Провести расчет')
        calc_menu.triggered.connect(self.calculate)
        # 1.2. График
        graph_menu = QtWidgets.QAction(save_ico, 'Сохранить график', self)
        graph_menu.setShortcut('Ctrl+A')
        graph_menu.setStatusTip('Сохранить график в JPG')
        # graph_menu.triggered.connect(self.close_event)
        # 1.3. Выбор методики
        method_menu = QtWidgets.QMenu('Выбор методики расчета', self)
        method_menu.setIcon(book_ico)
        # 1.3.1. Пожар пролива
        strait_fire_calc = QtWidgets.QAction(book_ico, 'Пожар пролива', self)
        strait_fire_calc.triggered.connect(self.change_method)
        method_menu.addAction(strait_fire_calc)
        # 1.3.2. Взрыв СП
        explosion_sp_calc = QtWidgets.QAction(book_ico, 'Взрыв (СП 12.13130-2009)', self)
        explosion_sp_calc.triggered.connect(self.change_method)
        method_menu.addAction(explosion_sp_calc)
        # 1.3.3. Взрыв ТВС
        explosion_tvs_calc = QtWidgets.QAction(book_ico, 'Взрыв (Методика ТВС)', self)
        explosion_tvs_calc.triggered.connect(self.change_method)
        method_menu.addAction(explosion_tvs_calc)
        # 1.3.4. Огненный шар
        fireball_calc = QtWidgets.QAction(book_ico, 'Огненный шар', self)
        fireball_calc.triggered.connect(self.change_method)
        # 1.3.4. Вспышка-НКПР
        lclp_calc = QtWidgets.QAction(book_ico, 'Пожар-вспышка', self)
        lclp_calc.triggered.connect(self.change_method)

        # Меню
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Файл')
        file_menu.addAction(calc_menu)
        file_menu.addAction(graph_menu)
        # file_menu.addAction(exit_prog)
        method_menu = menubar.addMenu('Методики')
        method_menu.addAction(strait_fire_calc)
        method_menu.addAction(explosion_sp_calc)
        method_menu.addAction(explosion_tvs_calc)
        method_menu.addAction(fireball_calc)
        method_menu.addAction(lclp_calc)
        help_menu = menubar.addMenu('Справка')
        # help_menu.addAction(help_show)
        # help_menu.addAction(about_prog)

        if not parent:
            self.show()

    def table_data_view(self):
        header_list = ['Параметр', 'Значение']
        for header in header_list:
            item = QtWidgets.QTableWidgetItem(header)
            item.setBackground(QtGui.QColor(150, 225, 225))
            self.table_data.setHorizontalHeaderItem(header_list.index(header), item)

    def set_param_names_in_table(self):
        self.table_data.setRowCount(0)
        text = self.selected_method.text()
        methods = ['Пожар пролива', 'Взрыв (СП 12.13130-2009)', 'Взрыв (Методика ТВС)', 'Огненный шар', 'Пожар-вспышка']
        names = [('Площадь, м2', 'm, кг/(с*м2) ', 'Mmol, кг/кмоль', 'Ткип, град.С', 'Ветер, м/с'),
                 ('Масса, кг', 'Qсг, кДж/кг ', 'z, -'),
                 ('Класс в-ва', 'Класс прост-ва', 'Масса, кг', 'Qсг, кДж/кг', 'sigma, -', 'Энергозапас, -'),
                 ('Масса, кг', 'Ef, кВт/м2'), ('Масса, кг', 'Mmol, кг/кмоль', 'Ткип, град.С', 'НКПР, об.%')]
        rows_tuple = (5, 3, 6, 2, 4)

        ind = methods.index(text)
        name = names[ind]
        rows = rows_tuple[ind]

        for row in range(rows):
            self.table_data.insertRow(row)
            for col in range(2):
                if col == 0:
                    item = QtWidgets.QTableWidgetItem(name[row])
                    item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                    self.table_data.setItem(row, col, item)

    def change_method(self):
        text = self.sender().text()
        self.selected_method.setText(text)
        self.set_param_names_in_table()

    def get_data_in_table(self):
        if not self.chek_server():
            return
        self.table_data.setFocusPolicy(QtCore.Qt.NoFocus)
        data_list = []
        try:
            for row in range(self.table_data.rowCount()):
                data_list.append(self.table_data.item(row, 1).text().replace(',', '.'))
        except:
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText(f"Не все поля заполненны")
            msg.exec()
            return

        # Повека корректнос веденх значений
        text = self.selected_method.text()
        methods = ['Пожар пролива', 'Взрыв (СП 12.13130-2009)', 'Взрыв (Методика ТВС)', 'Огненный шар', 'Пожар-вспышка']
        chek = [(float, float, float, float, float), (float, float, float), (int, int, float, float, float, float),
                (float, float), (int, float, float, float)]
        ind = methods.index(text)

        for i in data_list:
            try:
                chek[ind][data_list.index(i)](i)
            except:
                msg = QtWidgets.QMessageBox(self)
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setWindowTitle("Информация")
                msg.setText(f"Не верно указана характеристика: {i}")
                msg.exec()
                return
        return data_list

    def chek_server(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((IP, 8888))
            sock.close()
            return True
        except:
            msg = QtWidgets.QMessageBox(self)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Информация")
            msg.setText(f"Нет подключения к серверу!")
            msg.exec()
            return False

    def recvall(self, sock):
        BUFF_SIZE = 4096  # 4 KiB
        data = b''
        while True:
            part = sock.recv(BUFF_SIZE)
            data += part
            if len(part) < BUFF_SIZE:
                break
        return data

    def get_zone_in_server(self, data: list):
        text = self.selected_method.text()
        methods = ['Пожар пролива', 'Взрыв (СП 12.13130-2009)', 'Взрыв (Методика ТВС)', 'Огненный шар', 'Пожар-вспышка']
        ind = methods.index(text)
        server_call = (2,5,8,11,12)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((IP, 8888))
        str = f'({server_call[ind]}, {data})'
        sock.send(bytes(str, encoding='utf-8'))
        res = self.recvall(sock)
        print(res.decode())
        sock.close()
        return res


    def get_data_for_graph_in_server(self, data: list):
        text = self.selected_method.text()
        methods = ['Пожар пролива', 'Взрыв (СП 12.13130-2009)', 'Взрыв (Методика ТВС)', 'Огненный шар', 'Пожар-вспышка']
        ind = methods.index(text)
        if ind == 0:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((IP, 8888))
            str = f'(1, {data})'
            sock.send(bytes(str, encoding='utf-8'))
            res = self.recvall(sock)
            print(res.decode())
            sock.close()
            return res
        elif ind == 1:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((IP, 8888))
            str = f'(4, {data})'
            sock.send(bytes(str, encoding='utf-8'))
            res = self.recvall(sock)
            print(res.decode())
            sock.close()
            return res

        elif ind == 1:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((IP, 8888))
            str = f'(7, {data})'
            sock.send(bytes(str, encoding='utf-8'))
            res = self.recvall(sock)
            print(res.decode())
            sock.close()
            return res

    def report(self, data: list):
        text = self.selected_method.text()
        methods = ['Пожар пролива', 'Взрыв (СП 12.13130-2009)', 'Взрыв (Методика ТВС)', 'Огненный шар', 'Пожар-вспышка']
        ind = methods.index(text)

        if ind == 0:
            return (f'Зона 10.5 кВт/м2 = {data[0]} м \n'
                    f'Зона 7.0 кВт/м2 = {data[1]} м \n'
                    f'Зона 4.2 кВт/м2 = {data[2]} м \n'
                    f'Зона 1.4 кВт/м2 = {data[3]} м \n')

        elif ind == 1:
            return (f'Зона 100 кПа = {data[0]} м \n'
                    f'Зона 53 кПа = {data[1]} м \n'
                    f'Зона 28 кПа = {data[2]} м \n'
                    f'Зона 12 кПа = {data[3]} м \n'
                    f'Зона 5 кПа = {data[4]} м \n'
                    f'Зона 3 кПа = {data[5]} м \n')

        elif ind == 2:
            return (f'Зона 100 кПа = {data[0]} м \n'
                    f'Зона 53 кПа = {data[1]} м \n'
                    f'Зона 28 кПа = {data[2]} м \n'
                    f'Зона 12 кПа = {data[3]} м \n'
                    f'Зона 5 кПа = {data[4]} м \n'
                    f'Зона 3 кПа = {data[5]} м \n')

        elif ind == 3:
            return (f'Зона 600 кДж/м2 = {data[0]} м \n'
                    f'Зона 320 кДж/м2 = {data[1]} м \n'
                    f'Зона 220 кДж/м2 = {data[2]} м \n'
                    f'Зона 120 кДж/м2 = {data[3]} м \n')

        elif ind == 4:
            return (f'Зона НКПР = {data[0]} м \n'
                    f'Зона Вспышки = {data[1]} м \n')

    def calculate(self):
        data_list = self.get_data_in_table()
        if data_list == None:
            return
        zone = self.get_zone_in_server(data_list)
        for_graph = self.get_data_for_graph_in_server(data_list)
        self.result_text.setPlainText(self.report(eval(zone)))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    main = Calc_gui()
    app.exec_()
