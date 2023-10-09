import sys

class ABOpening:
    def __init__(self):
        self.leavesEvaluated = 0

    def findBestMove(self, board, depth):
        bestMove = board
        bestEstimate = float('-inf')
        possibleMoves = self.generateMovesOpening(board)
        for move in possibleMoves:
            estimate = self.abMinMax(move, depth-1, bestEstimate, float("inf"))
            if estimate > bestEstimate:
                bestEstimate = estimate
                bestMove = move
        return (bestMove, self.leavesEvaluated, bestEstimate)

    def abMinMax(self, board, depth, alpha, beta):
        if depth == 0:
            self.leavesEvaluated += 1
            return self.staticEstimateOpening(board)
        bestEstimate = float('inf')
        possibleMoves = self.generateBlackMovesOpening(board)
        for move in possibleMoves:
            estimate = self.abMaxMin(move, depth - 1, alpha, beta)
            if estimate <= bestEstimate:
                bestEstimate = estimate
            if bestEstimate <= alpha:
                return bestEstimate
            beta = min(beta, bestEstimate)
        return bestEstimate

    def abMaxMin(self, board, depth, alpha, beta):
        if depth == 0:
            self.leavesEvaluated += 1
            return self.staticEstimateOpening(board)
        bestEstimate = float('-inf')
        possibleMoves = self.generateMovesOpening(board)
        for move in possibleMoves:
            estimate = self.abMinMax(move, depth - 1, alpha, beta)
            if estimate >= bestEstimate:
                bestEstimate = estimate
            if bestEstimate >= beta:
                return bestEstimate
            alpha = max(alpha, bestEstimate)
        return bestEstimate

    def generateMovesOpening(self, board):
        return self.generateAdd(board)

    def generateAdd(self, board):
        possibleMoves = []
        for location in range(18):
            if board[location] == 'x':
                if location == 0:
                    possibleBoard = 'W' + board[1:]
                elif location == 17:
                    possibleBoard = board[:17] + 'W'
                else:
                    possibleBoard = board[:location]+'W'+board[location+1:]
                #print(possibleBoard, len(possibleBoard))
                if self.closeMill(location, possibleBoard):
                    possibleMoves = self.generateRemove(possibleBoard, possibleMoves)
                else:
                    possibleMoves.append(possibleBoard)
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
        elif location == 15 and (board[9] == piece and board[12] == piece or (board[16] == piece and board[17] == piece)):
            return True
        elif location == 16 and ((board[10] == piece and board[13] == piece) or (board[15] == piece and board[17] == piece)):
            return True
        elif location == 17 and ((board[1] == piece and board[8] == piece) or (board[11] == piece and board[14] == piece) or (board[15] == piece and board[16] == piece)):
            return True
        else:
            return False

    def staticEstimateOpening(self, board):
        numWhitePieces = 0
        numBlackPieces = 0
        for piece in board:
            if piece =='W':
                numWhitePieces += 1
            elif piece == 'B':
                numBlackPieces += 1
        return (numWhitePieces - numBlackPieces)

    def swapPieces(self, board):
        boardAsList = [state for state in board]
        for location in range(18):
            if boardAsList[location] == 'B':
                boardAsList[location] = 'W';
            elif boardAsList[location] == 'W':
                boardAsList[location] = 'B';
        return ''.join(boardAsList)

    def generateBlackMovesOpening(self, board):
        swappedBoard = self.swapPieces(board)
        possibleMovesSwapped = self.generateMovesOpening(swappedBoard)
        #print(swappedBoard, possibleMovesSwapped)
        possibleMoves = []
        for move in possibleMovesSwapped:
            possibleMoves.append(self.swapPieces(move))
        #print(board, possibleMoves)
        return possibleMoves

inputFile = open(sys.argv[1], 'r')
outputFile = open(sys.argv[2], 'w')
depth = int(sys.argv[3])
boardPosition = inputFile.readline()
inputFile.close()
game = ABOpening()
bestMove, numPosEvaluated, bestEstimate = game.findBestMove(boardPosition, depth)
outputFile.write("Board Position: " + bestMove + "\nPositions evaluated by static estimate: " + str(numPosEvaluated) + "\nMINIMAX estimate: " + str(bestEstimate))
outputFile.close()
print("Board Position:", bestMove)
print("Positions evaluated by static estimate:", numPosEvaluated)
print("MINIMAX estimate:", bestEstimate)