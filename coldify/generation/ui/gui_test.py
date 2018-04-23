import sys
from PyQt4 import QtGui


class Example(QtGui.QWidget):
    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        grid = QtGui.QGridLayout()
        self.setLayout(grid)

        lbl1 = QtGui.QLabel('ZetCode', self)
        lbl2 = QtGui.QLabel('tutorials', self)
        lbl3 = QtGui.QLabel('for programmers', self)
        
        grid.addWidget(lbl1, 0, 0)
        grid.addWidget(lbl2, 1, 0)
        grid.addWidget(lbl3, 2, 0)

        self.move(300, 150)
        self.setWindowTitle('Absolute')


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
