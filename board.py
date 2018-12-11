from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint
from PyQt5.QtGui import QPainter

from piece import Piece

class Board(QFrame):
    msg2Statusbar = pyqtSignal(str)

    # todo set the board with and height in square
    boardWidth = 8
    boardHeight = 8
    Speed =300

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
        '''starts game'''
        if self.isPaused:
            return

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.resetGame()

        self.msg2Statusbar.emit(str("status message"))

        self.timer.start(Board.Speed, self)

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
        if self.boardArray[yValue][xValue] == 1 and self.current_turn == 1:
            self.resetPossibleMoves()
            self.move = []
            self.move.append(yValue)
            self.move.append(xValue)
            self.player1PossibleMoves(yValue,xValue)
            self.update()
        elif self.boardArray[yValue][xValue] == 2 and self.current_turn == 2:
            self.move = []
            self.move.append(yValue)
            self.move.append(xValue)
            self.player2PossibleMoves(yValue, xValue)
            self.update()
        else:
            print(self.move)
            if len(self.move) > 1 and self.possibleMoves[yValue][xValue] == True:
                self.move.append(yValue)
                self.move.append(xValue)
                print(self.move)
                if self.current_turn == 1:
                    self.player1Move()
                else:
                    self.player2Move()
            else:
                print('Not a Piece')
        # todo you could call some game logic here

    def player1PossibleMoves(self, yValue, xValue):
        if xValue == 7:
            if self.boardArray[yValue - 1][xValue - 1] == 2:
                if xValue - 1 != 0:
                    if self.boardArray[yValue - 2][xValue - 2] == 0:
                        self.possibleMoves[yValue - 2][xValue - 2] = True
                        print("Possible Moves:", self.possibleMoves)
            if self.boardArray[yValue - 1][xValue - 1] == 0:
                self.possibleMoves[yValue - 1][xValue - 1] = True
                print("Possible Moves:", self.possibleMoves)
        elif xValue == 0:
            if self.boardArray[yValue - 1][xValue + 1] == 2:
                if xValue + 1 != 7:
                    if self.boardArray[yValue - 2][xValue + 2] == 0:
                        self.possibleMoves[yValue - 2][xValue + 2] = True
                        print("Possible Moves:", self.possibleMoves)
            if self.boardArray[yValue - 1][xValue + 1] == 0:
                self.possibleMoves[yValue - 1][xValue + 1] = True
                print("Possible Moves:", self.possibleMoves)
        elif yValue == 7:
            pass
        elif yValue == 0:
            pass
        else:
            if self.boardArray[yValue - 1][xValue + 1] == 2:
                if xValue + 1 != 7:
                    if self.boardArray[yValue - 2][xValue + 2] == 0:
                        self.possibleMoves[yValue - 2][xValue + 2] = True
                        print("Possible Moves:", self.possibleMoves)
            if self.boardArray[yValue - 1][xValue - 1] == 2:
                if xValue - 1 != 0:
                    if self.boardArray[yValue - 2][xValue - 2] == 0:
                        self.possibleMoves[yValue - 2][xValue - 2] = True
                        print("Possible Moves:", self.possibleMoves)
            if self.boardArray[yValue - 1][xValue + 1] == 0:
                self.possibleMoves[yValue - 1][xValue + 1] = True
                print("Possible Moves:", self.possibleMoves)
            if self.boardArray[yValue - 1][xValue - 1] == 0:
                self.possibleMoves[yValue - 1][xValue - 1] = True
                print("Possible Moves:", self.possibleMoves)
        print(self.possibleMoves)

    def player2PossibleMoves(self, yValue, xValue):
        if xValue == 7:
            if self.boardArray[yValue + 1][xValue - 1] == 1:
                if xValue - 1 != 0:
                    if self.boardArray[yValue + 2][xValue - 2] == 0:
                        self.possibleMoves[yValue + 2][xValue - 2] = True
            if self.boardArray[yValue + 1][xValue - 1] == 0:
                self.possibleMoves[yValue + 1][xValue - 1] = True
        elif xValue == 0:
            if self.boardArray[yValue + 1][xValue + 1] == 1:
                if xValue + 1 != 7:
                    if self.boardArray[yValue + 2][xValue + 2] == 0:
                        self.possibleMoves[yValue + 2][xValue + 2] = True
            if self.boardArray[yValue + 1][xValue + 1] == 0:
                self.possibleMoves[yValue + 1][xValue + 1] = True
        elif yValue == 7:
            pass
        elif yValue == 0:
            pass
        else:
            if self.boardArray[yValue + 1][xValue + 1] == 1:
                if xValue + 1 != 7:
                    if self.boardArray[yValue + 2][xValue + 2] == 0:
                        self.possibleMoves[yValue + 2][xValue + 2] = True
            if self.boardArray[yValue + 1][xValue - 1] == 1:
                if xValue - 1 != 0:
                    if self.boardArray[yValue + 2][xValue - 2] == 0:
                        self.possibleMoves[yValue + 2][xValue - 2] = True
            if self.boardArray[yValue + 1][xValue + 1] == 0:
                self.possibleMoves[yValue + 1][xValue + 1] = True
            if self.boardArray[yValue + 1][xValue - 1] == 0:
                self.possibleMoves[yValue + 1][xValue - 1] = True

    def player1Move(self):
        print('Player 1')
        from_y = self.move[0]
        from_x = self.move[1]
        to_y = self.move[2]
        to_x = self.move[3]
        if abs(from_y - to_y) == 2:
            self.boardArray[from_y][from_x] = 0
            self.boardArray[to_y][to_x] = 1
            if to_x > from_x:
                self.boardArray[to_y + 1][to_x - 1] = 0
            else:
                self.boardArray[to_y + 1][to_x + 1] = 0
        else:
            temp = self.boardArray[from_y][from_x]
            self.boardArray[from_y][from_x] = self.boardArray[to_y][to_x]
            self.boardArray[to_y][to_x] = temp
        self.update()
        self.move = []
        self.resetPossibleMoves()
        self.current_turn = 2



    def player2Move(self):
        print('Player 2')
        from_y = self.move[0]
        from_x = self.move[1]
        to_y = self.move[2]
        to_x = self.move[3]
        if abs(from_y - to_y) == 2:
            self.boardArray[from_y][from_x] = 0
            self.boardArray[to_y][to_x] = 2
            if to_x > from_x:
                self.boardArray[to_y - 1][to_x - 1] = 0
            else:
                self.boardArray[to_y - 1][to_x + 1] = 0
        else:
            temp = self.boardArray[from_y][from_x]
            self.boardArray[from_y][from_x] = self.boardArray[to_y][to_x]
            self.boardArray[to_y][to_x] = temp
        self.update()
        self.move = []
        self.resetPossibleMoves()
        self.current_turn = 1

    def keyPressEvent(self, event):
        '''processes key press events if you would like to do any'''
        if not self.isStarted or self.curPiece.shape() == Piece.NoPiece:
            super(Board, self).keyPressEvent(event)
            return

        key = event.key()

        if key == Qt.Key_P:
            self.pause()
            return

        if self.isPaused:
            return

        elif key == Qt.Key_Left:
            self.tryMove(self.curPiece, self.curX - 2, self.curY)

        elif key == Qt.Key_Right:
            self.tryMove(self.curPiece, self.curX + 1, self.curY)

        elif key == Qt.Key_Down:
            self.tryMove(self.curPiece.rotateRight(), self.curX, self.curY)

        elif key == Qt.Key_Up:
            self.tryMove(self.curPiece.rotateLeft(), self.curX, self.curY)

        elif key == Qt.Key_Space:
            self.dropDown()

        elif key == Qt.Key_D:
            self.oneLineDown()

        else:
            super(Board, self).keyPressEvent(event)

    def timerEvent(self, event):
        '''handles timer event'''
        #todo adapter this code to handle your timers

        if event.timerId() == self.timer.timerId():
            pass
        else:
            super(Board, self).timerEvent(event)

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
                colTransformation = col * self.squareWidth()  # Todo set this value equal the transformation you would like in the column direction
                rowTransformation = row * self.squareHeight()  # Todo set this value equal the transformation you would like in the column direction
                painter.save()
                painter.translate(colTransformation, rowTransformation)
                #Todo choose your colour and set the painter brush to the correct colour
                if self.boardArray[row][col] == 1:
                    colour = Qt.red
                elif self.boardArray[row][col] == 2:
                    colour = Qt.blue
                else:
                    colour = Qt.transparent
                painter.setBrush(colour)


                # Todo draw some the pieces as elipses
                radius1 = (self.squareWidth() - 2) / 2
                radius2 = (self.squareHeight() - 2) / 2
                # print(radius)
                center = QPoint(radius1, radius2)
                painter.drawEllipse(center, radius1, radius2)
                painter.restore()
