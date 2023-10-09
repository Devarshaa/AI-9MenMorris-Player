import sys


class MiniMaxGame:
    def __init__(self):
        self.leavesEvaluated = 0

    def maxMin(self, board, depth):
        if depth == 0:
            self.leavesEvaluated += 1
            return self.staticEstimateMidEnd(board)
        bestEstimate = float('-inf')
        # depth -= 1
        possibleMoves = self.generateMovesMidgameEndgame(board)
        # print('->', possibleMoves)
        for move in possibleMoves:
            estimate = self.minMax(move, depth - 1)
            if estimate >= bestEstimate:
                bestEstimate = estimate
        return bestEstimate

    def minMax(self, board, depth):
        if depth == 0:
            self.leavesEvaluated += 1
            return self.staticEstimateMidEnd(board)
        bestEstimate = float('inf')
        # depth -= 1
        possibleMoves = self.generateBlackMovesGame(board)
        # print('-->', possibleMoves)
        for move in possibleMoves:
            estimate = self.maxMin(move, depth - 1)
            if estimate <= bestEstimate:
                bestEstimate = estimate
        return bestEstimate

    def generateMovesMidgameEndgame(self, board):
        numWhitePieces = 0
        numBlackPieces = 0
        for location in board:
            if location == 'W':
                numWhitePieces += 1
            elif location == 'B':
                numBlackPieces += 1
        if numWhitePieces == 3:
            possibleMoves = self.generateHopping(board)
        else:
            possibleMoves = self.generateMove(board)
        return possibleMoves


    def generateHopping(self, board):
        possibleMoves = []
        positions = [state for state in board]
        for location in range(18):
            if board[location] == 'W':
                for location2 in range(18):
                    if board[location2] == 'x':
                        positions[location] = 'x'
                        positions[location2] = 'W'
                        possibleBoard = ''.join(positions)
                        positions[location] = 'W'
                        positions[location2] = 'x'
                        if self.closeMill(location2, possibleBoard):
                            possibleMoves = self.generateRemove(possibleBoard, possibleMoves)
                        else:
                            possibleMoves.append(possibleBoard)
                        #print(board, positions)
        #print("hop:", board, possibleMoves, len(possibleMoves))
        return possibleMoves

    def generateMove(self, board):
        possibleMoves = []
        positions = [state for state in board]
        for location in range(18):
            if board[location] == 'W':
                neighbours = self.neighbors(location)
                for neighbour in neighbours:
                    if board[neighbour] == 'x':
                        positions[location] = 'x'
                        positions[neighbour] = 'W'
                        possibleBoard = ''.join(positions)
                        positions[neighbour] = 'x'
                        positions[location] = 'W'
                        if self.closeMill(neighbour, possibleBoard):
                            #print('Mill closes')
                            possibleMoves = self.generateRemove(possibleBoard, possibleMoves)
                        else:
                            possibleMoves.append(possibleBoard)
                        #print(board, positions, possibleBoard)
        #print("move:",board, possibleMoves, len(possibleMoves))
        return possibleMoves

    def swapPieces(self, board):
        boardAsList = [state for state in board]
        for location in range(18):
            if boardAsList[location] == 'B':
                boardAsList[location] = 'W';
            elif boardAsList[location] == 'W':
                boardAsList[location] = 'B';
        return ''.join(boardAsList)


    def generateBlackMovesGame(self, board):
        swappedBoard = self.swapPieces(board)
        possibleMovesSwapped = self.generateMovesMidgameEndgame(swappedBoard)
        #print(swappedBoard, possibleMovesSwapped)
        possibleMoves = []
        for move in possibleMovesSwapped:
            possibleMoves.append(self.swapPieces(move))
        #print(board, possibleMoves)
        return possibleMoves

    def generateRemove(self, board, possibleMoves):
        opponentPieceAvailable = False
        for location in range(18):
            if board[location] == 'B' and not self.closeMill(location, board):
                opponentPieceAvailable = True
                if location == 0:
                    possibleBoard = 'x' + board[1:]
                elif location == 17:
                    possibleBoard = board[:17] + 'x'
                else:
                    possibleBoard = board[:location]+'x'+board[location+1:]
                #print(possibleBoard, len(possibleBoard), location)
                possibleMoves.append(possibleBoard)
        if not opponentPieceAvailable:
            possibleMoves.append(board)
        return possibleMoves

    def closeMill(self, location, board):
        piece = board[location]
        if location == 0 and (board[2] == piece and board[4] == piece):
            return True
        elif location == 1 and ((board[3] == piece and board[5] == piece) or (board[8] == piece and board[17] == piece)):
            return True
        elif location == 2 and (board[0] == piece and board[4] == piece):
            return True
        elif location == 3 and ((board[1] == piece and board[5] == piece) or (board[7] == piece and board[14] == piece)):
            return True
        elif location == 4 and (board[0] == piece and board[2] == piece):
            return True
        elif location == 5 and ((board[1] == piece and board[3] == piece) or (board[11] == piece and board[6] == piece)):
            return True
        elif location == 6 and ((board[7] == piece and board[8] == piece) or (board[5] == piece and board[11] == piece)):
            return True
        elif location == 7 and ((board[6] == piece and board[8] == piece) or (board[3] == piece and board[14] == piece)):
            return True
        elif location == 8 and ((board[6] == piece and board[7] == piece) or (board[1] == piece and board[17] == piece)):
            return True
        elif location == 9 and ((board[10] == piece and board[11] == piece) or (board[12] == piece and board[15] == piece)):
            return True
        elif location == 10 and ((board[9] == piece and board[11] == piece) or (board[13] == piece and board[16] == piece)):
            return True
        elif location == 11 and ((board[5] == piece and board[6] == piece) or (board[9] == piece and board[10] == piece) or (board[14] == piece and board[17] == piece)):
            return True
        elif location == 12 and ((board[9] == piece and board[15] == piece) or (board[13] == piece and board[14] == piece)):
            return True
        elif location == 13 and ((board[10] == piece and board[16] == piece) or (board[12] == piece and board[14] == piece)):
            return True
        elif location == 14 and ((board[3] == piece and board[7] == piece) or (board[12] == piece and board[13] == piece) or (board[11] == piece and board[17] == piece)):
            return True
        elif location == 15 and ((board[9] == piece and board[12] == piece) or (board[16] == piece and board[17] == piece)) :
            return True
        elif location == 16 and ((board[10] == piece and board[13] == piece) or (board[15] == piece and board[17] == piece)):
            return True
        elif location == 17 and ((board[1] == piece and board[8] == piece) or (board[11] == piece and board[14] == piece) or (board[15] == piece and board[16] == piece)):
            return True
        else:
            return False

    def neighbors(self, location):
        neighbourhood = []
        if location == 0:
            neighbourhood = [1, 2, 15]
        elif location == 1:
            neighbourhood = [0, 3, 8]
        elif location == 2:
            neighbourhood = [0, 3, 4, 12]
        elif location == 3:
            neighbourhood = [1, 2, 5, 7]
        elif location == 4:
            neighbourhood = [2, 5, 9]
        elif location == 5:
            neighbourhood = [3, 4, 6]
        elif location == 6:
            neighbourhood = [5, 7, 11]
        elif location == 7:
            neighbourhood = [3, 6, 8, 14]
        elif location == 8:
            neighbourhood = [1, 7, 17]
        elif location == 9:
            neighbourhood = [4, 10, 12]
        elif location == 10:
            neighbourhood = [9, 11, 13]
        elif location == 11:
            neighbourhood = [6, 10, 14]
        elif location == 12:
            neighbourhood = [2, 9, 13, 15]
        elif location == 13:
            neighbourhood = [10, 12, 14, 16]
        elif location == 14:
            neighbourhood = [7, 11, 13, 17]
        elif location == 15:
            neighbourhood = [0, 12, 16]
        elif location == 16:
            neighbourhood = [13, 15, 17]
        elif location == 17:
            neighbourhood = [8, 14, 16]
        return neighbourhood

    def findBestMove(self, board, depth):
        bestMove = board
        bestEstimate = float("-inf")
        possibleMoves = self.generateMovesMidgameEndgame(board)
        for move in possibleMoves:
            estimate = self.minMax(move, depth - 1)
            if estimate > bestEstimate:
                bestEstimate = estimate
                bestMove = move
        return bestMove, self.leavesEvaluated, bestEstimate

    def numberOfBlackMoves(self, board):
        swappedBoard = self.swapPieces(board)
        return len(self.generateMovesMidgameEndgame(swappedBoard))

    def staticEstimateMidEnd(self, board):
        numWhitePieces = 0
        numBlackPieces = 0
        numBlackMoves = self.numberOfBlackMoves(board)
        for piece in board:
            if piece == 'W':
                numWhitePieces += 1
            elif piece == 'B':
                numBlackPieces += 1
        if numWhitePieces <= 2:
            return -10000
        elif numBlackPieces <= 2 or numBlackMoves == 0:
            return 10000
        else:
            return (1000*(numWhitePieces - numBlackPieces) - numBlackMoves)


inputFile = open(sys.argv[1], 'r')
outputFile = open(sys.argv[2], 'w')
depth = int(sys.argv[3])
boardPosition = inputFile.readline()
inputFile.close()
game = MiniMaxGame()
#print(boardPosition)
bestMove, numPosEvaluated, bestEstimate = game.findBestMove(boardPosition, depth)
outputFile.write("Board Position: " + bestMove + "\nPositions evaluated by static estimate: " + str(numPosEvaluated) + "\nMINIMAX estimate: " + str(bestEstimate))
outputFile.close()
print("Board Position:", bestMove)
print("Positions evaluated by static estimate:", numPosEvaluated)
print("MINIMAX estimate:", bestEstimate)