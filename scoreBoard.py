from PyQt5.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import pyqtSlot
import datetime

class ScoreBoard(QDockWidget): # base the scoreboard on a QDockWidget

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''initiates ScoreBoard UI'''
        self.resize(200, 200)
        self.center()
        self.setWindowTitle('ScoreBoard')
        #create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        #create two labels which will be updated by signals
        self.label_timeRemaining = QLabel("Time Remaining: 300")
        self.red_pieces = QLabel("Player 1 Pieces Remaining: 12")
        self.blue_pieces = QLabel("Player 2 Pieces Remaining: 12")
        self.current_Turn = QLabel("Your Turn Player 1")
        self.turn_Timer = QLabel("Turn is up in: 30")

        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.label_timeRemaining)
        self.mainLayout.addWidget(self.red_pieces)
        self.mainLayout.addWidget(self.blue_pieces)
        self.mainLayout.addWidget(self.current_Turn)
        self.mainLayout.addWidget(self.turn_Timer)

        self.setWidget(self.mainWidget)
        self.show()

    # you do not need to implement this method
    def center(self):
        '''centers the window on the screen'''

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.updateTimerSignal.connect(self.setTimeRemaining)
        board.updateTurnSignal.connect(self.setTurnTimer)
        board.updateBlueSignal.connect(self.setBlueRemaining)
        board.updateRedSignal.connect(self.setRedRemaining)
        board.updatePlayerSignal.connect(self.setPlayerTurn)

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemaining):
        '''updates the time remaining label to show the time remaining'''
        update = "Time Remaining: " + str(datetime.timedelta(seconds=timeRemaining))
        self.label_timeRemaining.setText(update)
        # print('slot '+update)
        # self.redraw()

    @pyqtSlot(int)
    def setRedRemaining(self, redcheckers):
        '''updates the pieces remaining for player 1'''
        update = "Player 1 Pieces Remaining: " + str(redcheckers)
        self.red_pieces.setText(update)
        print('slot ' + update)

    @pyqtSlot(int)
    def setBlueRemaining(self, bluecheckers):
        '''updates the pieces remaining for player 2'''
        update = "Player 2 Pieces Remaining: " + str(bluecheckers)
        self.blue_pieces.setText(update)
        print('slot ' + update)

    @pyqtSlot(int)
    def setPlayerTurn(self, current_player):
        '''updates time for players time'''
        update = "Your Turn Player: " + str(current_player)
        self.current_Turn.setText(update)

    @pyqtSlot(int)
    def setTurnTimer(self, time):
        '''updates time for players time'''
        update = "Turn is up in: " + str(datetime.timedelta(seconds=time))
        self.turn_Timer.setText(update)
