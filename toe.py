import pickle
import random
import sys

board = [""] * 9


def drawBoard(td):
    print("\n")
    for i in range(len(td)):
        if td[i] != "":
            print(td[i], end="")
        else:
            print("-", end="")

        if i == 2 or i == 5:
            print("\n---------")
        else:
            if i != 8:
                print(" I ", end="")
    print("\n")


def getPlayerMove():
    playerMove = int(input())
    if 1 <= playerMove <= 9 and board[playerMove - 1] == "":
        return playerMove
    print("non valid move")
    return getPlayerMove()


def checkDraw():
    return "" not in board


def checkwin():
    wins = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]
    for win in wins:
        a, b, c = win
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a]
    return None


def convertMoves(br):
    convertedList = []
    for i in br:
        if i == "":
            convertedList.append(0)
        elif i == "X":
            convertedList.append(1)
        elif i == "O":
            convertedList.append(2)
        else:
            print("sped")
            sys.exit()
    return tuple(convertedList)


def saveQTable(qTable):
    with open("qTable.pkl", "wb") as f:
        pickle.dump(qTable, f)


def loadQTable():
    try:
        with open("qTable.pkl", "rb") as f:
            return pickle.load(f)
    except:
        return {}


class ai:
    def __init__(self):
        self.A = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.qTable = loadQTable()
        self.epsilon = 0.0
        self.alpha = 0.2
        self.gamma = 0.9

        self.oldS = None
        self.lastAction = None

        self.winVal = 1
        self.lossVal = -1
        self.drawVal = 0.1
        self.punishment = -10

        emptyS = convertMoves(board)
        if emptyS not in self.qTable:
            self.qTable[emptyS] = [0.0] * 9

    def stateRepresentation(self):
        boardState = convertMoves(board)
        if boardState not in self.qTable:
            self.qTable[boardState] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    def greedyPolicy(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.A)
        else:
            qVals = self.qTable[convertMoves(state)]
            maxVal = max(qVals)
            actions = []
            for i, val in enumerate(qVals):
                if val == maxVal:
                    actions.append(i)
            return random.choice(actions)

    def reward(self, state, action, shouldMove):
        rs = convertMoves(state)
        win = checkwin()
        draw = checkDraw()

        if rs[action] == 1 or rs[action] == 2:
            print("played on used pos")
            return self.punishment

        if shouldMove:
            board[action] = "O"
            win = checkwin()
            draw = checkDraw()

        if win == "X":
            return self.lossVal
        if win == "O":
            return self.winVal
        if draw:
            return self.drawVal
        return 0.0

    def updateQtbl(self, s, a, r, sPrime, terminal):
        oldQ = self.qTable[s][a]

        if terminal:
            nextMax = 0.0
        else:
            if sPrime not in self.qTable:
                self.qTable[sPrime] = [0.0] * 9
            nextMax = max(self.qTable[sPrime])
        # getting temporal difference and applying learning rate
        nextQ = oldQ + self.alpha * (r + self.gamma * nextMax - oldQ)
        self.qTable[s][a] = nextQ

    def move(self, t):
        cs = convertMoves(board)
        self.stateRepresentation()

        if t:
            if self.oldS is not None and self.lastAction is not None:
                win = checkwin()
                draw = checkDraw()
                if win == "X":
                    r = self.lossVal
                elif win == "O":
                    r = self.winVal
                elif draw:
                    r = self.drawVal
                else:
                    r = 0.0
                self.updateQtbl(convertMoves(self.oldS), self.lastAction, r, cs, True)
            return

        while True:
            action = self.greedyPolicy(board)
            r = self.reward(board, action, False)

            if r == self.punishment:
                self.updateQtbl(cs, action, self.punishment, cs, False)
                continue

            board[action] = "O"

            if self.oldS is not None and self.lastAction is not None:
                self.updateQtbl(
                    convertMoves(self.oldS), self.lastAction, 0.0, cs, False
                )

            bbm = board.copy()
            bbm[action] = ""
            self.oldS = bbm
            self.lastAction = action
            break


def randomMover():
    while True:
        i = random.randint(0, 8)
        if board[i] == "":
            return i


def dnr():
    win = checkwin()
    if checkwin():
        drawBoard(board)
        print("win ", win)
        clanker.move(True)
        saveQTable(clanker.qTable)
        return True
    if checkDraw():
        print("draw")
        clanker.move(True)
        saveQTable(clanker.qTable)
        return True


def main():
    global board
    clanker.oldS = None
    clanker.lastAction = None
    board = ["", "", "", "", "", "", "", "", ""]
    while True:
        drawBoard(board)
        playerMove = getPlayerMove()
        # playerMove = randomMover()
        board[playerMove - 1] = "X"  # REMEMEBR THE -1 HERE ITS OFF FOR TESTING
        if dnr():
            break
        clanker.move(False)
        if dnr():
            break


if __name__ == "__main__":
    clanker = ai()
    main()
