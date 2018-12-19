from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint
from PyQt5.QtGui import QPainter

from piece import Piece

class Board(QFrame):
    updateTimerSignal = pyqtSignal(int)
    updateTurnSignal = pyqtSignal(int)
    updateBlueSignal = pyqtSignal(int)
    updateRedSignal = pyqtSignal(int)
    updatePlayerSignal = pyqtSignal(int)

    msg2Statusbar = pyqtSignal(str)
    # todo set the board with and height in square
    boardWidth = 8
    boardHeight = 8
    Speed = 300
    timerSpeed = 1000
    counter = 600
    turn = 30
    redpieces = 12
    bluepieces = 12

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        '''initiates board'''
        self.timer = QBasicTimer()
        self.isWaitingAfterLine = False

        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.resetGame()
        self.start()

        self.current_turn = 1
        self.boardArray = [[2,0,2,0,2,0,2,0],
                           [0,2,0,2,0,2,0,2],
                           [2,0,2,0,2,0,2,0],
                           [0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0],
                           [0,1,0,1,0,1,0,1],
                           [1,0,1,0,1,0,1,0],
                           [0,1,0,1,0,1,0,1]
                           ]
        # self.boardArray = [[0,0,0,0,0,0,0,0],
        #                    [0,2,0,0,0,0,0,0],
        #                    [0,0,1,0,3,0,0,0],
        #                    [0,1,0,0,0,0,0,0],
        #                    [0,0,0,0,0,0,0,0],
        #                    [0,0,0,0,0,0,0,0],
        #                    [0,0,0,0,0,0,0,0],
        #                    [0,0,0,0,0,0,0,0]
        #                    ]
        self.possibleMoves = [[False, False, False, False, False, False, False, False],
                              [False, False, False, False, False, False, False, False],
                              [False, False, False, False, False, False, False, False],
                              [False, False, False, False, False, False, False, False],
                              [False, False, False, False, False, False, False, False],
                              [False, False, False, False, False, False, False, False],
                              [False, False, False, False, False, False, False, False],
                              [False, False, False, False, False, False, False, False],
                                ]
        # 2d int/Piece array to story the state of the game
        self.move = []
        self.moves_available = False
        # self.printBoardArray()

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

    def printBoardArray(self):
        '''prints the boardArray in an arractive way'''
        # print("boardArray:")
        # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self, event):
        '''convert the mouse click event to a row and column'''
        # x_point = QMouseEvent.pos()
        # print("Test: "+self.squareWidth()/event.pos().x())

    def squareWidth(self):
        '''returns the width of one square in the board'''
        return self.contentsRect().width() / Board.boardWidth

    def squareHeight(self):
        '''returns the height of one squarein the board'''
        return self.contentsRect().height() / Board.boardHeight

    def start(self):
        if self.isPaused:
            return
        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.resetGame()
        self.msg2Statusbar.emit(str("Game Started"))
        self.timer.start(Board.timerSpeed, self)

    def pause(self):
        '''pauses game'''

        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer.stop()
            self.msg2Statusbar.emit("paused")

        else:
            self.timer.start(Board.Speed, self)
            self.msg2Statusbar.emit(str("status message"))
        self.update()

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.drawPossibleMoves(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        xValue = (int)(event.x()/self.squareWidth())
        yValue = (int)(event.y()/self.squareHeight())
        if self.boardArray[yValue][xValue] == 1 and self.current_turn == 1 and self.moves_available == False:
            self.updateTurnSignal.emit(Board.turn)
            self.resetPossibleMoves()
            self.move = []
            self.move.append(yValue)
            self.move.append(xValue)
            self.player1PossibleMoves(yValue,xValue)
            self.update()
        elif self.boardArray[yValue][xValue] == 2 and self.current_turn == 2 and self.moves_available == False:
            self.resetPossibleMoves()
            self.move = []
            self.move.append(yValue)
            self.move.append(xValue)
            self.player2PossibleMoves(yValue, xValue)
            self.update()
        elif self.boardArray[yValue][xValue] == 3 and self.current_turn == 1 and self.moves_available == False:
            self.resetPossibleMoves()
            self.move = []
            self.move.append(yValue)
            self.move.append(xValue)
            self.player1KingPossibleMoves(yValue, xValue)
            self.update()
        elif self.boardArray[yValue][xValue] == 4 and self.current_turn == 2 and self.moves_available == False:
            self.resetPossibleMoves()
            self.move = []
            self.move.append(yValue)
            self.move.append(xValue)
            self.player2KingPossibleMoves(yValue, xValue)
            self.update()
        else:
            if len(self.move) > 1 and self.possibleMoves[yValue][xValue] == True:
                self.move.append(yValue)
                self.move.append(xValue)
                if self.current_turn == 1:
                    self.player1Move()
                else:
                    self.player2Move()

    def player1PossibleMoves(self, yValue, xValue):
        if yValue == 0:
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



    def player1Move(self):
        Board.turn = 30
        from_y = self.move[0]
        from_x = self.move[1]
        to_y = self.move[2]
        to_x = self.move[3]
        if to_y == 0:
            self.boardArray[from_y][from_x] = 3
        if abs(from_y - to_y) == 2:
            if self.boardArray[from_y][from_x] == 1:
                self.boardArray[from_y][from_x] = 0
                self.boardArray[to_y][to_x] = 1
            else:
                self.boardArray[from_y][from_x] = 0
                self.boardArray[to_y][to_x] = 3
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
            if self.boardArray[to_y][to_x] == 1:
                self.player1ConsecutiveMoves(to_y,to_x)
            else:
                self.player1KingConsecutiveMoves(to_y,to_x)
        else:
            temp = self.boardArray[from_y][from_x]
            self.boardArray[from_y][from_x] = self.boardArray[to_y][to_x]
            self.boardArray[to_y][to_x] = temp
            self.update()
            self.move = []
            self.resetPossibleMoves()
            self.current_turn = 2
        # self.captureEvent()
        self.changeTurnEvent()

    def player2Move(self):
        Board.turn = 30
        from_y = self.move[0]
        from_x = self.move[1]
        to_y = self.move[2]
        to_x = self.move[3]
        if to_y == 7:
            self.boardArray[from_y][from_x] = 4
        if abs(from_y - to_y) == 2:
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
        #todo adapter this code to handle your timers
        if event.timerId() == self.timer.timerId():
            if (self.current_turn == 1 and Board.turn == 0):
                self.current_turn = 2
                self.changeTurnEvent()
                Board.turn = 30
            elif(self.current_turn == 2 and Board.turn == 0):
                self.current_turn = 2
                self.changeTurnEvent()
                Board.turn = 30
            Board.turn = Board.turn - 1
            self.updateTurnSignal.emit(Board.turn)
            if(Board.counter == 0):
                if(Board.bluepieces < Board.redpieces):
                    self.msg2Statusbar.emit(str("Game Over: Player 1 Wins"))
                elif(Board.bluepieces > Board.redpieces):
                    self.msg2Statusbar.emit(str("Game Over: Player 2 Wins"))
                else:
                    self.msg2Statusbar.emit(str("Game Over: Draw"))
            if(Board.bluepieces == 0):
                self.msg2Statusbar.emit(str("Game Over: Player 1 Wins"))

            if(Board.redpieces == 0):
                self.msg2Statusbar.emit(str("Game Over: Player 2 Wins"))
            Board.counter = Board.counter - 1
            # print('timerEvent()', Board.counter)
            self.updateTimerSignal.emit(Board.counter)
        else:
            super(Board, self).timerEvent(event)

    def captureEvent(self):
        '''handles player timer event'''
        if(self.current_turn == 1):
            Board.bluepieces = Board.bluepieces - 1
            self.updateBlueSignal.emit(Board.bluepieces)
            print('BluePiecesRemaining', Board.bluepieces)
        elif(self.current_turn == 2):
            Board.redpieces = Board.redpieces - 1
            self.updateRedSignal.emit(Board.redpieces)
            print('RedPiecesRemaining', Board.redpieces)

    def changeTurnEvent(self):
        '''handles player turn event'''
        self.updatePlayerSignal.emit(self.current_turn)


    def resetGame(self):
        '''clears pieces from the board'''
        # todo write code to reset game

    def tryMove(self, newX, newY):
        '''tries to move a piece'''

    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        # todo set the dafault colour of the brush
        default_colour = Qt.black
        for row in range(0, Board.boardHeight):
            if default_colour == Qt.black:
                default_colour = Qt.white
            else:
                default_colour = Qt.black
            for col in range (0, Board.boardWidth):
                # if self.possibleMoves[row][col] == True:
                #     default_colour = Qt.yellow
                painter.save()
                colTransformation = col * self.squareWidth()# Todo set this value equal the transformation you would like in the column direction
                rowTransformation = row * self.squareHeight()# Todo set this value equal the transformation you would like in the column direction
                painter.translate(colTransformation,rowTransformation)
                painter.fillRect(0,0,self.squareWidth(),self.squareHeight(), default_colour) # Todo provide the required arguements
                painter.restore()
                # todo change the colour of the brush so that a checkered board is drawn
                if default_colour == Qt.black:
                    default_colour = Qt.white
                else:
                    default_colour = Qt.black

    def drawPossibleMoves(self, painter):
        for row in range(0, Board.boardHeight):
            default_colour = Qt.transparent
            for col in range (0, Board.boardWidth):
                if self.possibleMoves[row][col] == True:
                    default_colour = Qt.green
                painter.save()
                colTransformation = col * self.squareWidth()# Todo set this value equal the transformation you would like in the column direction
                rowTransformation = row * self.squareHeight()# Todo set this value equal the transformation you would like in the column direction
                painter.translate(colTransformation,rowTransformation)
                painter.fillRect(0,0,self.squareWidth(),self.squareHeight(), default_colour) # Todo provide the required arguements
                painter.restore()
                default_colour = Qt.transparent


    def drawPieces(self, painter):
        '''draw the prices on the board'''
        colour = Qt.transparent
        painter.setPen(Qt.transparent)
        for row in range(0, len(self.boardArray)):
            for col in range (0, len(self.boardArray[0])):
                king_colour = Qt.transparent
                colTransformation = col * self.squareWidth()  # Todo set this value equal the transformation you would like in the column direction
                rowTransformation = row * self.squareHeight()  # Todo set this value equal the transformation you would like in the column direction
                painter.save()
                painter.translate(colTransformation, rowTransformation)
                #Todo choose your colour and set the painter brush to the correct colour
                if self.boardArray[row][col] == 1:
                    colour = Qt.red
                elif self.boardArray[row][col] == 2:
                    colour = Qt.blue
                elif self.boardArray[row][col] == 3:
                    colour = Qt.red
                    king_colour = Qt.darkRed
                elif self.boardArray[row][col] == 4:
                    colour = Qt.blue
                    king_colour = Qt.darkBlue
                else:
                    colour = Qt.transparent
                    king_colour = Qt.transparent
                painter.setBrush(colour)


                # Todo draw some the pieces as elipses
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
