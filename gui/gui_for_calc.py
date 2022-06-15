# -----------------------------------------------------------
# Класс GUI для визуализации результатов расчета на сервере
#
# (C) 2022 Kuznetsov Konstantin, Kazan , Russian Federation
# email kuznetsovkm@yandex.ru
# -----------------------------------------------------------
from PySide2 import QtWidgets, QtGui
import sys
import os
from pathlib import Path
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

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
        self.setFixedSize(1500, 1200)
        self.setWindowTitle('Safety calc (v.1.0)')
        self.setWindowIcon(self.main_ico)

        central_widget = QtWidgets.QWidget()
        grid = QtWidgets.QGridLayout(self)
        grid.setColumnStretch(0, 2)
        grid.setColumnStretch(1, 5)

        # 1.Окно ввода данных
        self.table_data = QtWidgets.QTableWidget(0, 3)
        self.table_data_view()  # фукция отрисовки заголовков таблицы
        # 2. Окно текстового результата и выбранная методика
        self.result_text = QtWidgets.QPlainTextEdit()
        self.selected_method = QtWidgets.QLabel()
        self.selected_method.setText('Текущая методика: Пожар пролива')
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
        sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])

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
        # graph_menu.triggered.connect(self.close_event)
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
        # strait_fire_calc.triggered.connect(self.db_create)
        method_menu.addAction(strait_fire_calc)
        # 1.3.2. Взрыв СП
        explosion_sp_calc = QtWidgets.QAction(book_ico, 'Взрыв (СП 12.13130-2009)', self)
        # explosion_sp_calc.triggered.connect(self.db_create)
        method_menu.addAction(explosion_sp_calc)
        # 1.3.3. Взрыв ТВС
        explosion_tvs_calc = QtWidgets.QAction(book_ico, 'Взрыв (Методика ТВС)', self)
        # explosion_tvs_calc.triggered.connect(self.db_create)
        method_menu.addAction(explosion_tvs_calc)
        # 1.3.4. Огненный шар
        fireball_calc = QtWidgets.QAction(book_ico, 'Огненный шар', self)
        # fireball_calc.triggered.connect(self.db_create)
        # 1.3.4. Вспышка-НКПР
        lclp_calc = QtWidgets.QAction(book_ico, 'Пожар-вспышка', self)
        # lclp_calc.triggered.connect(self.db_create)


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
        header_list = ['Параметр', 'Значение', 'Размерность']
        for header in header_list:
            item = QtWidgets.QTableWidgetItem(header)
            item.setBackground(QtGui.QColor(225, 225, 225))
            self.table_data.setHorizontalHeaderItem(header_list.index(header), item)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyle('Fusion')
    main = Calc_gui()
    app.exec_()