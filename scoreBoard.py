from PyQt5.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import pyqtSlot
import datetime

class ScoreBoard(QDockWidget): # base the scoreboard on a QDockWidget
    # Constructor for the ScoreBoard class
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # initiates ScoreBoard UI
        self.resize(200, 200)
        self.center()
        self.setWindowTitle('ScoreBoard')
        # create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()
        # Variables to hold the names of the players
        self.player1_name = ""
        self.player2_name = ""
        # create five labels which will be updated by signals
        self.label_timeRemaining = QLabel("Time Remaining Player 1: 0:05:00")
        self.label_player2Remaining = QLabel("Time Remaining Player 2: 0:05:00")
        self.red_pieces = QLabel("Player 1 Pieces Remaining: 12")
        self.blue_pieces = QLabel("Player 2 Pieces Remaining: 12")
        self.current_Turn = QLabel("Your Turn Player 1")
        # Adding Widgets to the Layout
        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.label_timeRemaining)
        self.mainLayout.addWidget(self.label_player2Remaining)
        self.mainLayout.addWidget(self.red_pieces)
        self.mainLayout.addWidget(self.blue_pieces)
        self.mainLayout.addWidget(self.current_Turn)

        self.setWidget(self.mainWidget)
        self.show()
    def center(self):
        '''centers the window on the screen'''
    # set the names of the players to p1 and p2
    def setNames(self,p1,p2):
        self.player1_name = p1
        self.player2_name = p2
    # make connections to the board class
    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.updateTimerSignal.connect(self.setTimeRemaining)
        board.updateP2TimerSignal.connect(self.setP2TimeRemaining)
        board.updateBlueSignal.connect(self.setBlueRemaining)
        board.updateRedSignal.connect(self.setRedRemaining)
        board.updatePlayerSignal.connect(self.setPlayerTurn)
    #
    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemaining):
        '''updates the time remaining label to show the time remaining for player 1'''
        update = self.player1_name + " Time Remaining: " + str(datetime.timedelta(seconds=timeRemaining))
        self.label_timeRemaining.setText(update)

    @pyqtSlot(int)
    def setP2TimeRemaining(self, timeRemaining):
        '''updates the time remaining label to show the time remaining for player 2'''
        update = self.player2_name + " Time Remaining: " + str(datetime.timedelta(seconds=timeRemaining))
        self.label_player2Remaining.setText(update)

    @pyqtSlot(int)
    def setRedRemaining(self, redcheckers):
        '''updates the pieces remaining for player 1'''
        update = self.player1_name + " Pieces Remaining: " + str(redcheckers)
        self.red_pieces.setText(update)
        # print('slot ' + update)

    @pyqtSlot(int)
    def setBlueRemaining(self, bluecheckers):
        '''updates the pieces remaining for player 2'''
        update = self.player2_name + " Pieces Remaining: " + str(bluecheckers)
        self.blue_pieces.setText(update)
        # print('slot ' + update)

    @pyqtSlot(int)
    def setPlayerTurn(self, current_player):
        '''updates which players turn it currently is'''
        if current_player == 1:
            update = "Your Turn: " + self.player1_name
        elif current_player == 2:
            update = "Your Turn: " + self.player2_name
        else:
            update = "Game Over!!"
        self.current_Turn.setText(update)


