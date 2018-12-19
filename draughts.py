from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QAction, QMessageBox, QInputDialog, QLineEdit, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from board import Board
from scoreBoard import ScoreBoard
import sys

class Draughts(QMainWindow):
    # Constructor for the Draughts class
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        '''initiates application UI'''
        self.tboard = Board(self)
        self.setCentralWidget(self.tboard)
        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.RightDockWidgetArea, self.scoreBoard)
        self.statusbar = self.statusBar()
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)
        self.scoreBoard.make_connection(self.tboard)

        self.tboard.start()
        # Making a menubar and adding file and help menus to it
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu(" File")
        helpMenu = mainMenu.addMenu(" Help")

        # add Pause action in the file menu pauses the game
        pauseAction = QAction(QIcon("./icons/pause.png"), "Pause/Resume", self)
        pauseAction.setShortcut("Ctrl+P")
        fileMenu.addAction(pauseAction)
        pauseAction.triggered.connect(self.tboard.pause)
        # add Reset action in the file menu resets the game
        resetAction = QAction(QIcon("./icons/reset.png"), "Reset", self)
        resetAction.setShortcut("Ctrl+R")
        fileMenu.addAction(resetAction)
        resetAction.triggered.connect(self.tboard.resetGame)
        # add about action in the help menu
        aboutAction = QAction(QIcon("./icons/about.png"), "About", self)
        aboutAction.setShortcut("Ctrl+A")
        helpMenu.addAction(aboutAction)
        aboutAction.triggered.connect(self.about)
        # add help action in the help menu
        helpAction = QAction(QIcon("./icons/help.png"), "Help", self)
        helpAction.setShortcut("Ctrl+H")
        helpMenu.addAction(helpAction)
        helpAction.triggered.connect(self.help)

        self.resize(800, 800)
        self.center()
        self.setWindowTitle('Checkers')
        self.setWindowIcon(QIcon("./icons/checkers.png"))
        self.show()
        # getting the names of the 2 players
        self.p1_name = self.getPlayer1Name()
        self.p2_name = self.getPlayer2Name()
        # sending the names of the players to the board and scoreBoard classes
        self.tboard.setNames(self.p1_name,self.p2_name)
        self.scoreBoard.setNames(self.p1_name,self.p2_name)
        # geting the color combination for the pieces
        color_combo = self.getChoice()
        # sending the color combination to the board class
        self.tboard.pieceColors(color_combo)
        # make a connection between scoreBoard and board
        self.scoreBoard.make_connection(self.tboard)
        # start the game
        self.tboard.start()

    # asks the user to choose between color combinations
    def getChoice(self):
        items = ("P1:Red / P2:Cyan", "P1:Green / P2:Pink", "P1:Blue / P2:Yellow")
        item, okPressed = QInputDialog.getItem(self, "Get item", "Color:", items, 0, False)
        if okPressed and item:
            print(item)
            if item == "P1:Red / P2:Cyan":
                print(1)
                return 1
            elif item == "P1:Green / P2:Pink":
                print(2)
                return 2
            else:
                print(3)
                return 3
        else:
            self.getChoice()
    # asks player 1 for their name
    def getPlayer1Name(self):
        text, okPressed = QInputDialog.getText(self, "Player 1 Name", "Enter your name:", QLineEdit.Normal, "")
        if okPressed and text != "":
            text = text.capitalize()
            return text
        else:
            self.getPlayer1Name()

    # asks player 2 for their name
    def getPlayer2Name(self):
        text, okPressed = QInputDialog.getText(self, "Player 2 Name", "Enter your name:", QLineEdit.Normal, "")
        if okPressed and text == self.p1_name:
            return self.getPlayer2Name()
        elif okPressed and text != "":
            text = text.capitalize()
            return text
        else:
            self.getPlayer2Name()

    def center(self):
        '''centers the window on the screen'''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)
    # the about message box
    def about(self):
        QMessageBox.about(self, "About","Checkers is a board game played between two people on an 8x8 checked board like the one shown below."
                                        "\nEach player has 12 pieces that are like flat round disks that fit inside each of the boxes on the board. "
                                        "The pieces are placed on every other dark square and then staggered by rows, like shown on the board. ")
    # the help message box
    def help(self):
        QMessageBox.about(self, "Help", """Taking a Turn:
        \nEach player takes their turn by moving a piece. Pieces are always moved diagonally and can be moved in the following ways: 
        \n-Diagonally in the forward direction (towards the opponent) to the next dark square.
        \n-If there is one of the opponent's pieces next to a piece and an empty space on the other side, you jump your opponent and remove their piece. You can do multiple jumps if they are lined up in the forward direction. 
        \nNote: if you have a jump, you have no choice but to take it.
        \nKing Pieces:
        \nThe last row is called the king row. If you get a piece across the board to the opponent's king row, that piece becomes a king. Another piece is placed onto that piece so it is now two pieces high. King pieces can move in both directions, forward and backward. 
        \nOnce a piece is kinged, the player must wait until the next turn to jump out of the king row. 
        \nWinning the Game:
        \nYou win the game when the opponent has no more pieces or can't move (even if he/she still has pieces). If neither player can move then it is a draw or a tie. """)
