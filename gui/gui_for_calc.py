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


class Calc_gui(QtWidgets.QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__()
        self.main_ico = QtGui.QIcon(str(Path(os.getcwd()).parents[0]) + '\ico\calc.png')
        print(str(Path(os.getcwd()).parents[0]))
        # Главное окно
        self.setFixedSize(900, 700)
        self.setWindowTitle('Safety calc (v.1.0)')
        self.setWindowIcon(self.main_ico)

        # Меню
        # Меню приложения (верхняя плашка)
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Файл')
        # file_menu.addMenu(db_menu)
        # file_menu.addMenu(plan_menu)
        # file_menu.addAction(exit_prog)
        view_menu = menubar.addMenu('Вид')
        # view_menu.addAction(scale_plus)
        # view_menu.addAction(scale_min)
        # view_menu.addAction(hand_act)
        edit_menu = menubar.addMenu('Объект')
        # edit_menu.addAction(del_end_point)
        # edit_menu.addAction(del_all_point)
        # edit_menu.addAction(save_obj)
        # edit_menu.addAction(del_obj)
        draw_menu = menubar.addMenu('Рисование')
        # draw_menu.addAction(draw_all)
        # draw_menu.addAction(draw_one)
        # draw_menu.addAction(draw_risk)
        help_menu = menubar.addMenu('Справка')
        # help_menu.addAction(help_show)
        # help_menu.addAction(about_prog)

        if not parent:
            self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyle('Fusion')
    main = Calc_gui()
    app.exec_()