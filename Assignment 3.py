from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
import sys, random
from PyQt5.QtCore import Qt, QPoint, QSize
# default window class
class Checkers(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.tboard = Board(self)
        self.setCentralWidget(self.tboard)

        self.statusbar = self.statusBar()
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)

        # self.tboard.start()

        self.resize(380, 380)
        self.center()
        self.setWindowTitle('Checkers')
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,(screen.height() - size.height()) / 2)


class Board(QFrame):
    msg2Statusbar = pyqtSignal(str)

    BoardWidth = 22
    BoardHeight = 22

    def __init__(self, parent):
        super().__init__(parent)

        self.initBoard()

    def initBoard(self):
        pass

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = Checkers()
    window.show()
    app.exec()
