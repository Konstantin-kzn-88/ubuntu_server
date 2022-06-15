from time import sleep

from PySide2 import QtWidgets, QtGui, QtCore
import sys

class Calc_gui(QtWidgets.QMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__()
        self.selected_method = QtWidgets.QLabel()
        self.selected_method.setText("Пожар")
        self.setCentralWidget(self.selected_method)
        self.change()
        if not parent:
            self.show()


    def change(self):
        sleep(3)
        print(self.selected_method.text())

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = Calc_gui()
    app.exec_()