from PyQt5.QtWidgets import QFrame, QMainWindow, QDesktopWidget, QApplication, QAction, QMessageBox, QInputDialog, QLineEdit, QDockWidget, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint, pyqtSlot
from PyQt5.QtGui import QPainter, QIcon
import sys
import datetime

class Board(QFrame):
    # Creates connections with the scoreboard class
    updateTimerSignal = pyqtSignal(int)
    updateP2TimerSignal = pyqtSignal(int)
    updateBlueSignal = pyqtSignal(int)
    updateRedSignal = pyqtSignal(int)
    updatePlayerSignal = pyqtSignal(int)
    msg2Statusbar = pyqtSignal(str)
    # constant Variables for the board class
    boardWidth = 8
    boardHeight = 8
    # variables for scoreboard
    Speed = 300
    timerSpeed = 1000
    counter = 300
    p2counter = 300
    turn = 30
    redpieces = 12
    bluepieces = 12

    # Constructor for the board class
    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        '''initiates board'''
        # initializes basic timer
        self.timer = QBasicTimer()
        self.isWaitingAfterLine = False
        self.setFocusPolicy(Qt.StrongFocus)
        # checker variables to check if paused or started
        self.isStarted = False
        self.isPaused = False
        # default colors for the player pieces
        self.player1_color = Qt.transparent
        self.player1_king_color = Qt.transparent
        self.player2_color = Qt.transparent
        self.player2_king_color = Qt.transparent
        self.possible_move_color = Qt.transparent
        # default names for the players
        self.player1_name = ""
        self.player2_name = ""
        # current turn variable
        self.current_turn = 1
        # board array
        self.boardArray = [[2,0,2,0,2,0,2,0],
                           [0,2,0,2,0,2,0,2],
                           [2,0,2,0,2,0,2,0],
                           [0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0],
                           [0,1,0,1,0,1,0,1],
                           [1,0,1,0,1,0,1,0],
                           [0,1,0,1,0,1,0,1]
                           ]
        # possible moves array
        self.possibleMoves = [[False, False, False, False, False, False, False, False],
                              [False, False, False, False, False, False, False, False],
                              [False, False, False, False, False, False, False, False],
                              [False, False, False, False, False, False, False, False],
                              [False, False, False, False, False, False, False, False],
                              [False, False, False, False, False, False, False, False],
                              [False, False, False, False, False, False, False, False],
                              [False, False, False, False, False, False, False, False],
                                ]
        # move list to store the to and from locations on the board
        self.move = []
        # variable to check if a consecutive move is possible
        self.moves_available = False
    # setting the names of the players to p1 and p2
    def setNames(self,p1,p2):
        self.player1_name = p1
        self.player2_name = p2
    # reset the possible moves array
    def resetPossibleMoves(self):
        self.possibleMoves = [[False, False, False, False, False, False, False, False],
                              [False, False, False, False, False, False, False, False],
                              [False, False, False, False, False, False, False, False],
                              [False, False, False, False, False, False, False, False],
                              [False, False, False, False, False, False, False, False],
                              [False, False, False, False, False, False, False, False],
                              [False, False, False, False, False, False, False, False],
                              [False, False, False, False, False, False, False, False],
                              ]
    # reset the board array
    def resetBoard(self):
        self.boardArray = [[2, 0, 2, 0, 2, 0, 2, 0],
                           [0, 2, 0, 2, 0, 2, 0, 2],
                           [2, 0, 2, 0, 2, 0, 2, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 1, 0, 1, 0, 1, 0, 1],
                           [1, 0, 1, 0, 1, 0, 1, 0],
                           [0, 1, 0, 1, 0, 1, 0, 1]
                           ]
    # returns the square width of the board
    def squareWidth(self):
        '''returns the width of one square in the board'''
        return self.contentsRect().width() / Board.boardWidth

    # returns the square heigth of the board
    def squareHeight(self):
        '''returns the height of one squarein the board'''
        return self.contentsRect().height() / Board.boardHeight
    # method that starts the game
    def start(self):
        if self.isPaused:
            return
        self.isStarted = True
        self.resetGame()
        self.msg2Statusbar.emit(str("Game Started"))
        self.timer.start(Board.timerSpeed, self)
    # this method pauses the game and timers
    def pause(self):
        '''pauses game'''
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer.stop()
            self.msg2Statusbar.emit("Paused")

        else:
            self.timer.start(Board.Speed, self)
            self.msg2Statusbar.emit(str("Running"))
        self.update()
    # this method resets the whole game to the beginning
    def resetGame(self):
        '''clears pieces from the board'''
        self.resetBoard()
        self.resetPossibleMoves()
        self.move = []
        self.moves_available = False
        Board.counter = 300
        Board.p2counter = 300
        Board.redpieces = 12
        Board.bluepieces = 12
        self.updateRedSignal.emit(Board.redpieces)
        self.updateBlueSignal.emit(Board.bluepieces)
        self.updateTimerSignal.emit(Board.counter)
        self.updateP2TimerSignal.emit(Board.p2counter)
        self.current_turn = 1
        self.updatePlayerSignal.emit(self.current_turn)
        self.update()
    # setting the colors of the pieces and possible moves to the color combo chosen by the user
    def pieceColors(self,num):
        if num == 1:
            self.player1_color = Qt.red
            self.player1_king_color = Qt.darkRed
            self.player2_color = Qt.cyan
            self.player2_king_color = Qt.darkCyan
            self.possible_move_color = Qt.yellow
        elif num == 2:
            self.player1_color = Qt.green
            self.player1_king_color = Qt.darkGreen
            self.player2_color = Qt.magenta
            self.player2_king_color = Qt.darkMagenta
            self.possible_move_color = Qt.blue
        else:
            self.player1_color = Qt.blue
            self.player1_king_color = Qt.darkBlue
            self.player2_color = Qt.yellow
            self.player2_king_color = Qt.darkYellow
            self.possible_move_color = Qt.red
        self.update()
    # method paints on the painter widget
    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        # calls on method to draw the board
        self.drawBoardSquares(painter)
        # calls on method to draw the possible moves
        self.drawPossibleMoves(painter)
        # calls on method to draw the pieces
        self.drawPieces(painter)
    # this method is called whenever there is a mouse click
    def mousePressEvent(self, event):
        # if the game is paused do nothing
        if self.isPaused == True:
            return
        # takes the sqaure index of where the click happened
        xValue = (int)(event.x()/self.squareWidth())
        yValue = (int)(event.y()/self.squareHeight())
        # checks if a player 1 piece was clicked during player 1 turn and also if a consecutove move isn't possible rn
        if self.boardArray[yValue][xValue] == 1 and self.current_turn == 1 and self.moves_available == False:
            # reset possible moves and the move list
            self.resetPossibleMoves()
            self.move = []
            # append the x y values of the piece you clicked
            self.move.append(yValue)
            self.move.append(xValue)
            # call on the possible moves method to check where the piece can move to
            self.player1PossibleMoves(yValue,xValue)
            self.update()
        # this does the same as the previous if statement but for player 2
        elif self.boardArray[yValue][xValue] == 2 and self.current_turn == 2 and self.moves_available == False:
            self.resetPossibleMoves()
            self.move = []
            self.move.append(yValue)
            self.move.append(xValue)
            self.player2PossibleMoves(yValue, xValue)
            self.update()
        # this does the same as the previous if statements but for player 1 king pieces
        elif self.boardArray[yValue][xValue] == 3 and self.current_turn == 1 and self.moves_available == False:
            self.resetPossibleMoves()
            self.move = []
            self.move.append(yValue)
            self.move.append(xValue)
            self.player1KingPossibleMoves(yValue, xValue)
            self.update()
        # this does the same as the previous if statements but for player 2 king pieces
        elif self.boardArray[yValue][xValue] == 4 and self.current_turn == 2 and self.moves_available == False:
            self.resetPossibleMoves()
            self.move = []
            self.move.append(yValue)
            self.move.append(xValue)
            self.player2KingPossibleMoves(yValue, xValue)
            self.update()
        else:
            # checks if theres already a click location in the move list
            # if there is that means the second click is the location to move the piece to
            # and checks if the click was a possible move
            if len(self.move) > 1 and self.possibleMoves[yValue][xValue] == True:
                # append the second location to the move list
                self.move.append(yValue)
                self.move.append(xValue)
                # call on the players move method depending on whos turn it is
                if self.current_turn == 1:
                    self.player1Move()
                else:
                    self.player2Move()
    # checks every possible move for player 1 according to the x and y values
    def player1PossibleMoves(self, yValue, xValue):
        # if the piece is at the top dont check for moves
        if yValue == 0:
            pass
        # if piece is on the far right side of the board only check left for moves
        elif xValue == 7:
            if self.boardArray[yValue - 1][xValue - 1] == 2 or self.boardArray[yValue - 1][xValue - 1] == 4:
                if yValue - 1 != 0:
                    if self.boardArray[yValue - 2][xValue - 2] == 0:
                        self.possibleMoves[yValue - 2][xValue - 2] = True
            if self.boardArray[yValue - 1][xValue - 1] == 0:
                self.possibleMoves[yValue - 1][xValue - 1] = True
        # if piece is on the far right side of the board only check left for moves
        elif xValue == 0:
            if self.boardArray[yValue - 1][xValue + 1] == 2 or self.boardArray[yValue - 1][xValue + 1] == 4:
                if yValue - 1 != 0:
                    if self.boardArray[yValue - 2][xValue + 2] == 0:
                        self.possibleMoves[yValue - 2][xValue + 2] = True
            if self.boardArray[yValue - 1][xValue + 1] == 0:
                self.possibleMoves[yValue - 1][xValue + 1] = True
        # check for moves in accordance to checker rules
        else:
            capture_available = False
            if self.boardArray[yValue - 1][xValue + 1] == 2 or self.boardArray[yValue - 1][xValue + 1] == 4:
                if xValue + 1 != 7 and yValue - 1 != 0:
                    if self.boardArray[yValue - 2][xValue + 2] == 0:
                        self.possibleMoves[yValue - 2][xValue + 2] = True
                        capture_available = True
            if self.boardArray[yValue - 1][xValue - 1] == 2 or self.boardArray[yValue - 1][xValue - 1] == 4:
                if xValue - 1 != 0 and yValue - 1 != 0:
                    if self.boardArray[yValue - 2][xValue - 2] == 0:
                        self.possibleMoves[yValue - 2][xValue - 2] = True
                        capture_available = True
            if capture_available == False:
                if self.boardArray[yValue - 1][xValue + 1] == 0:
                    self.possibleMoves[yValue - 1][xValue + 1] = True
                if self.boardArray[yValue - 1][xValue - 1] == 0:
                    self.possibleMoves[yValue - 1][xValue - 1] = True

    # does the same as the previous method except its for player 2
    def player2PossibleMoves(self, yValue, xValue):
        if yValue == 7:
                # or yValue == 6:
            pass
        elif xValue == 7:
            if self.boardArray[yValue + 1][xValue - 1] == 1 or self.boardArray[yValue + 1][xValue - 1] == 3:
                if yValue + 1 != 7:
                    if self.boardArray[yValue + 2][xValue - 2] == 0:
                        self.possibleMoves[yValue + 2][xValue - 2] = True
            if self.boardArray[yValue + 1][xValue - 1] == 0:
                self.possibleMoves[yValue + 1][xValue - 1] = True
        elif xValue == 0:
            if self.boardArray[yValue + 1][xValue + 1] == 1 or self.boardArray[yValue + 1][xValue + 1] == 3:
                if yValue + 1 != 7:
                    if self.boardArray[yValue + 2][xValue + 2] == 0:
                        self.possibleMoves[yValue + 2][xValue + 2] = True
            if self.boardArray[yValue + 1][xValue + 1] == 0:
                self.possibleMoves[yValue + 1][xValue + 1] = True
        else:
            capture_available = False
            if self.boardArray[yValue + 1][xValue + 1] == 1 or self.boardArray[yValue + 1][xValue + 1] == 3:
                if xValue + 1 != 7 and yValue + 1 != 7:
                    if self.boardArray[yValue + 2][xValue + 2] == 0:
                        self.possibleMoves[yValue + 2][xValue + 2] = True
                        capture_available = True
            if self.boardArray[yValue + 1][xValue - 1] == 1 or self.boardArray[yValue + 1][xValue - 1] == 3:
                if xValue - 1 != 0 and yValue + 1 != 7:
                    if self.boardArray[yValue + 2][xValue - 2] == 0:
                        self.possibleMoves[yValue + 2][xValue - 2] = True
                        capture_available = True
            if capture_available == False:
                if self.boardArray[yValue + 1][xValue + 1] == 0:
                    self.possibleMoves[yValue + 1][xValue + 1] = True
                if self.boardArray[yValue + 1][xValue - 1] == 0:
                    self.possibleMoves[yValue + 1][xValue - 1] = True

    # does the same as the player 1 possible moves method except except it checks forwards and backwards for theking pieces
    def player1KingPossibleMoves(self, yValue, xValue):
        capture_available = False
        if yValue == 0:
                # or yValue == 1:
            pass
        elif xValue == 7:
            if self.boardArray[yValue - 1][xValue - 1] == 2 or self.boardArray[yValue - 1][xValue - 1] == 4:
                if yValue - 1 != 0:
                    if self.boardArray[yValue - 2][xValue - 2] == 0:
                        self.possibleMoves[yValue - 2][xValue - 2] = True
            if self.boardArray[yValue - 1][xValue - 1] == 0:
                self.possibleMoves[yValue - 1][xValue - 1] = True
        elif xValue == 0:
            if self.boardArray[yValue - 1][xValue + 1] == 2 or self.boardArray[yValue - 1][xValue + 1] == 4:
                if yValue - 1 != 0:
                    if self.boardArray[yValue - 2][xValue + 2] == 0:
                        self.possibleMoves[yValue - 2][xValue + 2] = True
            if self.boardArray[yValue - 1][xValue + 1] == 0:
                self.possibleMoves[yValue - 1][xValue + 1] = True
        else:
            if self.boardArray[yValue - 1][xValue + 1] == 2 or self.boardArray[yValue - 1][xValue + 1] == 4:
                if xValue + 1 != 7 and yValue - 1 != 0:
                    if self.boardArray[yValue - 2][xValue + 2] == 0:
                        self.possibleMoves[yValue - 2][xValue + 2] = True
                        capture_available = True
            if self.boardArray[yValue - 1][xValue - 1] == 2 or self.boardArray[yValue - 1][xValue - 1] == 4:
                if xValue - 1 != 0 and yValue - 1 != 0:
                    if self.boardArray[yValue - 2][xValue - 2] == 0:
                        self.possibleMoves[yValue - 2][xValue - 2] = True
                        capture_available = True
        if yValue == 7:
                # or yValue == 6:
            pass
        elif xValue == 7:
            if self.boardArray[yValue + 1][xValue - 1] == 2 or self.boardArray[yValue + 1][xValue - 1] == 4:
                if yValue + 1 != 7:
                    if self.boardArray[yValue + 2][xValue - 2] == 0:
                        self.possibleMoves[yValue + 2][xValue - 2] = True
            if self.boardArray[yValue + 1][xValue - 1] == 0:
                self.possibleMoves[yValue + 1][xValue - 1] = True
        elif xValue == 0:
            if self.boardArray[yValue + 1][xValue + 1] == 2 or self.boardArray[yValue + 1][xValue + 1] == 4:
                if yValue + 1 != 7:
                    if self.boardArray[yValue + 2][xValue + 2] == 0:
                        self.possibleMoves[yValue + 2][xValue + 2] = True
            if self.boardArray[yValue + 1][xValue + 1] == 0:
                self.possibleMoves[yValue + 1][xValue + 1] = True
        else:
            if self.boardArray[yValue + 1][xValue + 1] == 2 or self.boardArray[yValue + 1][xValue + 1] == 4:
                if xValue + 1 != 7 and yValue + 1 != 7:
                    if self.boardArray[yValue + 2][xValue + 2] == 0:
                        self.possibleMoves[yValue + 2][xValue + 2] = True
                        capture_available = True
            if self.boardArray[yValue + 1][xValue - 1] == 2 or self.boardArray[yValue + 1][xValue - 1] == 4:
                if xValue - 1 != 0 and yValue + 1 != 7:
                    if self.boardArray[yValue + 2][xValue - 2] == 0:
                        self.possibleMoves[yValue + 2][xValue - 2] = True
                        capture_available = True
        if yValue != 0 and capture_available == False:
            if xValue != 7:
                if self.boardArray[yValue - 1][xValue + 1] == 0:
                    self.possibleMoves[yValue - 1][xValue + 1] = True
            if xValue != 0:
                if self.boardArray[yValue - 1][xValue - 1] == 0:
                    self.possibleMoves[yValue - 1][xValue - 1] = True
        if yValue != 7 and capture_available == False:
            if xValue != 7:
                if self.boardArray[yValue + 1][xValue + 1] == 0:
                    self.possibleMoves[yValue + 1][xValue + 1] = True
            if xValue != 0:
                if self.boardArray[yValue + 1][xValue - 1] == 0:
                    self.possibleMoves[yValue + 1][xValue - 1] = True

    # does the same as the previous method except its for player 2
    def player2KingPossibleMoves(self, yValue, xValue):
        capture_available = False
        if yValue == 7:
                # or yValue == 6:
            pass
        elif xValue == 7:
            if self.boardArray[yValue + 1][xValue - 1] == 1 or self.boardArray[yValue + 1][xValue - 1] == 3:
                if yValue + 1 != 7:
                    if self.boardArray[yValue + 2][xValue - 2] == 0:
                        self.possibleMoves[yValue + 2][xValue - 2] = True
            if self.boardArray[yValue + 1][xValue - 1] == 0:
                self.possibleMoves[yValue + 1][xValue - 1] = True
        elif xValue == 0:
            if self.boardArray[yValue + 1][xValue + 1] == 1 or self.boardArray[yValue + 1][xValue + 1] == 3:
                if yValue + 1 != 7:
                    if self.boardArray[yValue + 2][xValue + 2] == 0:
                        self.possibleMoves[yValue + 2][xValue + 2] = True
            if self.boardArray[yValue + 1][xValue + 1] == 0:
                self.possibleMoves[yValue + 1][xValue + 1] = True
        else:
            if self.boardArray[yValue + 1][xValue + 1] == 1 or self.boardArray[yValue + 1][xValue + 1] == 3:
                if xValue + 1 != 7 and yValue + 1 != 7:
                    if self.boardArray[yValue + 2][xValue + 2] == 0:
                        self.possibleMoves[yValue + 2][xValue + 2] = True
                        capture_available = True
            if self.boardArray[yValue + 1][xValue - 1] == 1 or self.boardArray[yValue + 1][xValue - 1] == 3:
                if xValue - 1 != 0 and yValue + 1 != 7:
                    if self.boardArray[yValue + 2][xValue - 2] == 0:
                        self.possibleMoves[yValue + 2][xValue - 2] = True
                        capture_available = True

        if yValue == 0:
                # or yValue == 1:
            pass
        elif xValue == 7:
            if self.boardArray[yValue - 1][xValue - 1] == 1 or self.boardArray[yValue - 1][xValue - 1] == 3:
                if yValue - 1 != 0:
                    if self.boardArray[yValue - 2][xValue - 2] == 0:
                        self.possibleMoves[yValue - 2][xValue - 2] = True
            if self.boardArray[yValue - 1][xValue - 1] == 0:
                self.possibleMoves[yValue - 1][xValue - 1] = True
        elif xValue == 0:
            if self.boardArray[yValue - 1][xValue + 1] == 1 or self.boardArray[yValue - 1][xValue + 1] == 3:
                if yValue - 1 != 0:
                    if self.boardArray[yValue - 2][xValue + 2] == 0:
                        self.possibleMoves[yValue - 2][xValue + 2] = True
            if self.boardArray[yValue - 1][xValue + 1] == 0:
                self.possibleMoves[yValue - 1][xValue + 1] = True
        else:
            if self.boardArray[yValue - 1][xValue + 1] == 1 or self.boardArray[yValue - 1][xValue + 1] == 3:
                if xValue + 1 != 7 and yValue - 1 != 0:
                    if self.boardArray[yValue - 2][xValue + 2] == 0:
                        self.possibleMoves[yValue - 2][xValue + 2] = True
                        capture_available = True
            if self.boardArray[yValue - 1][xValue - 1] == 1 or self.boardArray[yValue - 1][xValue - 1] == 3:
                if xValue - 1 != 0 and yValue - 1 != 0:
                    if self.boardArray[yValue - 2][xValue - 2] == 0:
                        self.possibleMoves[yValue - 2][xValue - 2] = True
                        capture_available = True
        if yValue != 0 and capture_available == False:
            if xValue != 7:
                if self.boardArray[yValue - 1][xValue + 1] == 0:
                    self.possibleMoves[yValue - 1][xValue + 1] = True
            if xValue != 0:
                if self.boardArray[yValue - 1][xValue - 1] == 0:
                    self.possibleMoves[yValue - 1][xValue - 1] = True
        if yValue != 7 and capture_available == False:
            if xValue != 7:
                if self.boardArray[yValue + 1][xValue + 1] == 0:
                    self.possibleMoves[yValue + 1][xValue + 1] = True
            if xValue != 0:
                if self.boardArray[yValue + 1][xValue - 1] == 0:
                    self.possibleMoves[yValue + 1][xValue - 1] = True


    # method for moving player 1 pieces
    def player1Move(self):
        # location of the starting click
        from_y = self.move[0]
        from_x = self.move[1]
        # location of the second click
        to_y = self.move[2]
        to_x = self.move[3]
        # if piece reaches the top make it a king piece
        if to_y == 0:
            self.boardArray[from_y][from_x] = 3
        # checks if piece captured enemy piece
        if abs(from_y - to_y) == 2:
            # updates how many pieces each player has on the board for the scoreboard
            self.captureEvent()
            # if piece is regular piece move it to new location
            if self.boardArray[from_y][from_x] == 1:
                self.boardArray[from_y][from_x] = 0
                self.boardArray[to_y][to_x] = 1
            # else its a king piece move it to new location
            else:
                self.boardArray[from_y][from_x] = 0
                self.boardArray[to_y][to_x] = 3
            # determines direction of the move and removes enemy piece according to the direction
            if to_x > from_x:
                if to_y > from_y:
                    self.boardArray[to_y - 1][to_x - 1] = 0
                else:
                    self.boardArray[to_y + 1][to_x - 1] = 0
            else:
                if to_y > from_y:
                    self.boardArray[to_y - 1][to_x + 1] = 0
                else:
                    self.boardArray[to_y + 1][to_x + 1] = 0
            # reset moves and possible moves then check for consecutive moves
            self.update()
            self.move = []
            self.resetPossibleMoves()
            if self.boardArray[to_y][to_x] == 1:
                self.player1ConsecutiveMoves(to_y,to_x)
            else:
                self.player1KingConsecutiveMoves(to_y,to_x)
        # this is if the move was a regular move not a capture
        else:
            # just move the piece to the new location
            temp = self.boardArray[from_y][from_x]
            self.boardArray[from_y][from_x] = self.boardArray[to_y][to_x]
            self.boardArray[to_y][to_x] = temp
            # change turns and reset the moves and possible moves
            self.update()
            self.move = []
            self.resetPossibleMoves()
            self.current_turn = 2
            self.changeTurnEvent()
    # same as the previous method but for its player 2
    def player2Move(self):
        from_y = self.move[0]
        from_x = self.move[1]
        to_y = self.move[2]
        to_x = self.move[3]
        if to_y == 7:
            self.boardArray[from_y][from_x] = 4
        if abs(from_y - to_y) == 2:
            self.captureEvent()
            if self.boardArray[from_y][from_x] == 2:
                self.boardArray[from_y][from_x] = 0
                self.boardArray[to_y][to_x] = 2
            else:
                self.boardArray[from_y][from_x] = 0
                self.boardArray[to_y][to_x] = 4
            if to_x > from_x:
                if to_y > from_y:
                    self.boardArray[to_y - 1][to_x - 1] = 0
                else:
                    self.boardArray[to_y + 1][to_x - 1] = 0
            else:
                if to_y > from_y:
                    self.boardArray[to_y - 1][to_x + 1] = 0
                else:
                    self.boardArray[to_y + 1][to_x + 1] = 0
            self.update()
            self.move = []
            self.resetPossibleMoves()
            if self.boardArray[to_y][to_x] == 2:
                self.player2ConsecutiveMoves(to_y,to_x)
            else:
                self.player2KingConsecutiveMoves(to_y,to_x)
        else:
            temp = self.boardArray[from_y][from_x]
            self.boardArray[from_y][from_x] = self.boardArray[to_y][to_x]
            self.boardArray[to_y][to_x] = temp
            self.update()
            self.move = []
            self.resetPossibleMoves()
            self.current_turn = 1
        # self.captureEvent()
        self.changeTurnEvent()
    # checks for possible consecutive moves its the same as the possible moves method except it only checks for captures
    def player1ConsecutiveMoves(self,yValue,xValue):
        if yValue == 0 or yValue == 1:
            pass
        elif xValue == 7:
            if self.boardArray[yValue - 1][xValue - 1] == 2:
                if self.boardArray[yValue - 2][xValue - 2] == 0:
                    self.possibleMoves[yValue - 2][xValue - 2] = True
        elif xValue == 0:
            if self.boardArray[yValue - 1][xValue + 1] == 2:
                if self.boardArray[yValue - 2][xValue + 2] == 0:
                    self.possibleMoves[yValue - 2][xValue + 2] = True
        else:
            if self.boardArray[yValue - 1][xValue + 1] == 2:
                if xValue + 1 != 7:
                    if self.boardArray[yValue - 2][xValue + 2] == 0:
                        self.possibleMoves[yValue - 2][xValue + 2] = True
            if self.boardArray[yValue - 1][xValue - 1] == 2:
                if xValue - 1 != 0:
                    if self.boardArray[yValue - 2][xValue - 2] == 0:
                        self.possibleMoves[yValue - 2][xValue - 2] = True
        self.moves_available = False
        for i in self.possibleMoves:
            for j in i:
                if j == True:
                    self.moves_available = True

        if self.moves_available == True:
            self.move.append(yValue)
            self.move.append(xValue)
        else:
            self.current_turn = 2
    # same as previous method except its for player 2
    def player2ConsecutiveMoves(self,yValue,xValue):
        if yValue == 7 or yValue == 6:
            pass
        elif xValue == 7:
            if self.boardArray[yValue + 1][xValue - 1] == 1:
                if self.boardArray[yValue + 2][xValue - 2] == 0:
                    self.possibleMoves[yValue + 2][xValue - 2] = True
        elif xValue == 0:
            if self.boardArray[yValue + 1][xValue + 1] == 1:
                if self.boardArray[yValue + 2][xValue + 2] == 0:
                    self.possibleMoves[yValue + 2][xValue + 2] = True
        else:
            if self.boardArray[yValue + 1][xValue + 1] == 1:
                if xValue + 1 != 7:
                    if self.boardArray[yValue + 2][xValue + 2] == 0:
                        self.possibleMoves[yValue + 2][xValue + 2] = True
            if self.boardArray[yValue + 1][xValue - 1] == 1:
                if xValue - 1 != 0:
                    if self.boardArray[yValue + 2][xValue - 2] == 0:
                        self.possibleMoves[yValue + 2][xValue - 2] = True
        self.moves_available = False
        for i in self.possibleMoves:
            for j in i:
                if j == True:
                    self.moves_available = True

        if self.moves_available == True:
            self.move.append(yValue)
            self.move.append(xValue)
        else:
            self.current_turn = 1

    # does teh same as player 1 consecutive moves method except it checks forwards and backwards for king pieces
    def player1KingConsecutiveMoves(self,yValue,xValue):
        if yValue == 0:
            pass
        elif xValue == 7:
            if self.boardArray[yValue - 1][xValue - 1] == 2 or self.boardArray[yValue - 1][xValue - 1] == 4:
                if yValue - 1 != 0:
                    if self.boardArray[yValue - 2][xValue - 2] == 0:
                        self.possibleMoves[yValue - 2][xValue - 2] = True
        elif xValue == 0:
            if self.boardArray[yValue - 1][xValue + 1] == 2 or self.boardArray[yValue - 1][xValue + 1] == 4:
                if yValue - 1 != 0:
                    if self.boardArray[yValue - 2][xValue + 2] == 0:
                        self.possibleMoves[yValue - 2][xValue + 2] = True
        else:
            if self.boardArray[yValue - 1][xValue + 1] == 2 or self.boardArray[yValue - 1][xValue + 1] == 4:
                if xValue + 1 != 7 and yValue - 1 != 0:
                    if self.boardArray[yValue - 2][xValue + 2] == 0:
                        self.possibleMoves[yValue - 2][xValue + 2] = True
            if self.boardArray[yValue - 1][xValue - 1] == 2 or self.boardArray[yValue - 1][xValue - 1] == 4:
                if xValue - 1 != 0 and yValue - 1 != 0:
                    if self.boardArray[yValue - 2][xValue - 2] == 0:
                        self.possibleMoves[yValue - 2][xValue - 2] = True
        if yValue == 7:
            pass
        elif xValue == 7:
            if self.boardArray[yValue + 1][xValue - 1] == 2 or self.boardArray[yValue + 1][xValue - 1] == 4:
                if yValue + 1 != 7:
                    if self.boardArray[yValue + 2][xValue - 2] == 0:
                        self.possibleMoves[yValue + 2][xValue - 2] = True
        elif xValue == 0:
            if self.boardArray[yValue + 1][xValue + 1] == 2 or self.boardArray[yValue + 1][xValue + 1] == 4:
                if yValue + 1 != 7:
                    if self.boardArray[yValue + 2][xValue + 2] == 0:
                        self.possibleMoves[yValue + 2][xValue + 2] = True
        else:
            if self.boardArray[yValue + 1][xValue + 1] == 2 or self.boardArray[yValue + 1][xValue + 1] == 4:
                if xValue + 1 != 7 and yValue + 1 != 7:
                    if self.boardArray[yValue + 2][xValue + 2] == 0:
                        self.possibleMoves[yValue + 2][xValue + 2] = True
            if self.boardArray[yValue + 1][xValue - 1] == 2 or self.boardArray[yValue + 1][xValue - 1] == 4:
                if xValue - 1 != 0 and yValue + 1 != 7:
                    if self.boardArray[yValue + 2][xValue - 2] == 0:
                        self.possibleMoves[yValue + 2][xValue - 2] = True
        self.moves_available = False
        for i in self.possibleMoves:
            for j in i:
                if j == True:
                    self.moves_available = True

        if self.moves_available == True:
            self.move.append(yValue)
            self.move.append(xValue)
        else:
            self.current_turn = 2

    # same as previous method except its for player 2
    def player2KingConsecutiveMoves(self,yValue,xValue):
        if yValue == 7:
                # or yValue == 6:
            pass
        elif xValue == 7:
            if self.boardArray[yValue + 1][xValue - 1] == 1 or self.boardArray[yValue + 1][xValue - 1] == 3:
                if yValue + 1 != 7:
                    if self.boardArray[yValue + 2][xValue - 2] == 0:
                        self.possibleMoves[yValue + 2][xValue - 2] = True
        elif xValue == 0:
            if self.boardArray[yValue + 1][xValue + 1] == 1 or self.boardArray[yValue + 1][xValue + 1] == 3:
                if yValue + 1 != 7:
                    if self.boardArray[yValue + 2][xValue + 2] == 0:
                        self.possibleMoves[yValue + 2][xValue + 2] = True
        else:
            if self.boardArray[yValue + 1][xValue + 1] == 1 or self.boardArray[yValue + 1][xValue + 1] == 3:
                if xValue + 1 != 7 and yValue + 1 != 7:
                    if self.boardArray[yValue + 2][xValue + 2] == 0:
                        self.possibleMoves[yValue + 2][xValue + 2] = True
            if self.boardArray[yValue + 1][xValue - 1] == 1 or self.boardArray[yValue + 1][xValue - 1] == 3:
                if xValue - 1 != 0 and yValue + 1 != 7:
                    if self.boardArray[yValue + 2][xValue - 2] == 0:
                        self.possibleMoves[yValue + 2][xValue - 2] = True
        if yValue == 0:
            pass
        elif xValue == 7:
            if self.boardArray[yValue - 1][xValue - 1] == 1 or self.boardArray[yValue - 1][xValue - 1] == 3:
                if yValue - 1 != 0:
                    if self.boardArray[yValue - 2][xValue - 2] == 0:
                        self.possibleMoves[yValue - 2][xValue - 2] = True
        elif xValue == 0:
            if self.boardArray[yValue - 1][xValue + 1] == 1 or self.boardArray[yValue - 1][xValue + 1] == 3:
                if yValue - 1 != 0:
                    if self.boardArray[yValue - 2][xValue + 2] == 0:
                        self.possibleMoves[yValue - 2][xValue + 2] = True
        else:
            if self.boardArray[yValue - 1][xValue + 1] == 1 or self.boardArray[yValue - 1][xValue + 1] == 3:
                if xValue + 1 != 7 and yValue - 1 != 0:
                    if self.boardArray[yValue - 2][xValue + 2] == 0:
                        self.possibleMoves[yValue - 2][xValue + 2] = True
            if self.boardArray[yValue - 1][xValue - 1] == 1 or self.boardArray[yValue - 1][xValue - 1] == 3:
                if xValue - 1 != 0 and yValue - 1 != 0:
                    if self.boardArray[yValue - 2][xValue - 2] == 0:
                        self.possibleMoves[yValue - 2][xValue - 2] = True
        self.moves_available = False
        for i in self.possibleMoves:
            for j in i:
                if j == True:
                    self.moves_available = True

        if self.moves_available == True:
            self.move.append(yValue)
            self.move.append(xValue)
        else:
            self.current_turn = 1

    def timerEvent(self, event):
        '''handles timer event'''
        # dont start timer if game isnt started
        if self.isStarted == False:
            return
        # makes sure that the timer IDs are the same
        if event.timerId() == self.timer.timerId():
            if(self.current_turn == 1):
                # decrement the counter for player 1
                Board.counter = Board.counter - 1
                # update timer in the scoreboard
                self.updateTimerSignal.emit(Board.counter)
                # if timer runs out execute win conditon
                if (Board.counter == 0):
                    self.msg2Statusbar.emit(self.player2_name + " Wins, " + self.player1_name + " Ran out of Time.")
                    self.current_turn = 0
                    self.updatePlayerSignal(self.current_turn)
            # same as previous if statement except its for player 2
            elif(self.current_turn == 2):
                Board.p2counter = Board.p2counter - 1
                self.updateP2TimerSignal.emit(Board.p2counter)
                if (Board.p2counter == 0):
                    self.msg2Statusbar.emit(self.player1_name + " Wins, " + self.player2_name + " Ran out of Time.")
                    self.current_turn = 0
                    self.updatePlayerSignal(self.current_turn)
        else:
            super(Board, self).timerEvent(event)

    def captureEvent(self):
        '''handles capturing event'''
        # if player 1 decrement player 2 pieces and update the scoreboard
        if(self.current_turn == 1):
            Board.bluepieces = Board.bluepieces - 1
            self.updateBlueSignal.emit(Board.bluepieces)
            # if player 2 has no more pieces call on win condition
            if (Board.bluepieces == 0):
                self.msg2Statusbar.emit(self.player1_name + " Wins, " + self.player1_name + " Captured all Enemy Pieces.")
                self.finished = True
        # same except its for player 2
        elif(self.current_turn == 2):
            Board.redpieces = Board.redpieces - 1
            self.updateRedSignal.emit(Board.redpieces)
            if (Board.redpieces == 0):
                self.msg2Statusbar.emit(self.player2_name + " Wins, " + self.player2_name + " Captured all Enemy Pieces.")
                self.finished = True

    def changeTurnEvent(self):
        '''handles player turn event'''
        self.updatePlayerSignal.emit(self.current_turn)

    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        # set default color
        default_colour = Qt.white
        for row in range(0, Board.boardHeight):
            # switch color at the beginning of each row
            if default_colour == Qt.black:
                default_colour = Qt.white
            else:
                default_colour = Qt.black
            for col in range (0, Board.boardWidth):
                painter.save()
                # column and row transformations
                colTransformation = col * self.squareWidth()
                rowTransformation = row * self.squareHeight()
                # draw sqaures according to the row and col transformation
                painter.translate(colTransformation,rowTransformation)
                painter.fillRect(0,0,self.squareWidth(),self.squareHeight(), default_colour)
                painter.restore()
                # switch color at the beginning of each col
                if default_colour == Qt.black:
                    default_colour = Qt.white
                else:
                    default_colour = Qt.black

    def drawPossibleMoves(self, painter):
        # draws the possible moves on the board if they exist
        for row in range(0, Board.boardHeight):
            # set default color
            default_colour = Qt.transparent
            for col in range (0, Board.boardWidth):
                # if possible move exists change color
                if self.possibleMoves[row][col] == True:
                    default_colour = self.possible_move_color
                # draw the possible move on the board
                painter.save()
                colTransformation = col * self.squareWidth()
                rowTransformation = row * self.squareHeight()
                painter.translate(colTransformation,rowTransformation)
                painter.fillRect(0,0,self.squareWidth(),self.squareHeight(), default_colour)
                painter.restore()
                default_colour = Qt.transparent


    def drawPieces(self, painter):
        '''draw the prices on the board'''
        # set default color
        colour = Qt.transparent
        painter.setPen(Qt.transparent)
        for row in range(0, len(self.boardArray)):
            for col in range (0, len(self.boardArray[0])):
                # sets default color for the king
                king_colour = Qt.transparent
                colTransformation = col * self.squareWidth()
                rowTransformation = row * self.squareHeight()
                painter.save()
                painter.translate(colTransformation, rowTransformation)
                # if current location is a piece set the color of the piece
                if self.boardArray[row][col] == 1:
                    colour = self.player1_color
                elif self.boardArray[row][col] == 2:
                    colour = self.player2_color
                elif self.boardArray[row][col] == 3:
                    colour = self.player1_color
                    king_colour = self.player1_king_color
                elif self.boardArray[row][col] == 4:
                    colour = self.player2_color
                    king_colour = self.player2_king_color
                else:
                    colour = Qt.transparent
                    king_colour = Qt.transparent
                # draw the pieces
                painter.setBrush(colour)
                radius1 = (self.squareWidth() - 2) / 2
                radius2 = (self.squareHeight() - 2) / 2
                center = QPoint(radius1, radius2)
                painter.drawEllipse(center, radius1, radius2)
                painter.setBrush(king_colour)
                # radius1 = (self.squareWidth() - 20) / 2
                # radius2 = (self.squareHeight() - 20) / 2
                center = QPoint(radius1, radius2)
                painter.drawEllipse(center, radius1/1.4, radius2/1.4)
                painter.restore()

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


app = QApplication([])
draughts = Draughts()
sys.exit(app.exec_())