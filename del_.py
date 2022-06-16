from PySide2 import QtWidgets, QtCore
import pyqtgraph as pg


class Window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.setGeometry(300, 100, 600, 600)
        self.setWindowTitle('Программа')

        hbox = QtWidgets.QHBoxLayout()
        self.button_ = QtWidgets.QPushButton('Run')
        self.button_.clicked.connect(self.change)

        self.my_layout = pg.GraphicsLayoutWidget()
        self.my_layout.setBackground('w')
        pen = pg.mkPen(color=(150, 255, 0), width=15, style=QtCore.Qt.DashLine)

        hour1 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        temperature1 = [3, 3, 3, 4, 4, 5, 5, 5, 5, 5]

        hour2 = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        temperature2 = [3, 3, 3, 4, 4, 5, 5, 5, 5, 5]

        self.g1 = self.my_layout.addPlot(x=hour1, y=temperature1, pen = pen, symbol='+', symbolSize=30, row=0, col=0, title="Plot @ row 1, column 1")
        self.g2 = self.my_layout.addPlot(x=hour2, y=temperature2, row=0, col=1, title="Plot @ row 1, column 2")

        styles = {'color': 'r', 'font-size': '20px'}
        self.g2.setLabel('left', 'Temperature (°C)', **styles)
        self.g2.setLabel('bottom', 'Hour (H)', **styles)

        hbox.addWidget(self.my_layout)
        hbox.addWidget(self.button_)

        self.setLayout(hbox)

    def change(self):
        hour1 = [5, 20, 150, 240, 350, 460, 870, 980, 1090, 1100]
        temperature1 = [3, 7, 3, 7, 4, 6, 5, 5, 5, 1]
        pen = pg.mkPen(color=(0, 150, 150), width=15, style=QtCore.Qt.DashLine)

        self.my_layout.removeItem(self.g1)
        self.g1 = self.my_layout.addPlot(x=hour1, y=temperature1, pen=pen, symbol='+', symbolSize=30, row=0, col=0,
                                         title="Plot @ row 1, column 1")

        self.my_layout.clear()



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = Window()
    w.show()
    app.exec_()
