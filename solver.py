import tkinter as tk
import random
import copy

import colors as c
import ai		

class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)	
        self.grid()	
        self.master.title('2048 AI')	
        self.master.resizable(False, False)	
        self.mainGrid = tk.Frame(
            self, 
            bg = c.gridColor,
            bd = 3,
            width = 600,
            height = 600)		
        self.mainGrid.grid(row = 0, column = 0, pady = (100, 0))	

        self.makeGUI()		
        self.startGame()	
        self.updateGUI()	
        self.after(2000, self.autoPlay)	

    def makeGUI(self):
        self.cells = []	
        for i in range(4):
            row = []		
            for j in range(4):
                cellFrame = tk.Frame(
                    self.mainGrid,
                    bg = c.emptyCellColor,
                    width = 150,
                    height = 150)	
                cellFrame.grid(row = i, column = j, padx = 5, pady = 5)		
                cellNumber = tk.Label(self.mainGrid)	
                cellNumber.grid(row = i, column = j)	
                cellData = {'frame': cellFrame, 'number': cellNumber}		
                row.append(cellData)		
            self.cells.append(row)	

        scoreFrame = tk.Frame(self)	
        scoreFrame.place(relx = 0.5, y = 45, anchor = "center")		
        tk.Label(
            scoreFrame,
            text = "Score",
            font = c.scoreLabelFont).grid(row = 0)	
        self.scoreLabel = tk.Label(scoreFrame, text = "0", font = c.scoreFont)	
        self.scoreLabel.grid(row = 1)		

        movesFrame = tk.Frame(self, bd = 2, relief = "sunken")	
        movesFrame.grid(row = 0, column = 1, sticky = "ns", padx = (10, 0))		
        tk.Label(movesFrame, text = "AI Moves", font = ("Verdana", 16)).pack()		

        self.movesCanvas = tk.Canvas(movesFrame, width = 100)		
        self.movesScrollbar = tk.Scrollbar(
            movesFrame, orient = "vertical", command = self.movesCanvas.yview)		

        self.movesScrollbar.pack(side = "right", fill = "y")	
        self.movesCanvas.pack(side = "left", fill = "both", expand = True)	

        self.movesCanvas.configure(yscrollcommand = self.movesScrollbar.set)	
        self.movesFrameInner = tk.Frame(self.movesCanvas)		
        self.movesCanvas.create_window(

            (0, 0), 
            window = self.movesFrameInner, 
            anchor = "nw")	
        self.movesFrameInner.bind("<Configure>", 
            lambda event: self.movesCanvas.configure(scrollregion = self.movesCanvas.bbox("all")))		

        self.moveCount = 0	
        self.moveLabels = []	

        exportButton = tk.Button(
            movesFrame, text = "Export Moves", command = self.exportMoves)	
        exportButton.pack(pady = 10)	

    def startGame(self):
        self.matrix = [[0] * 4 for _ in range(4)]	
        self.addNewTile()		
        self.addNewTile()	
        self.score = 0		
        self.movesList = []		

    def stack(self, matrix):
        newMatrix = [[0]*4 for _ in range(4)]	
        for i in range(4):
            pos = 0	
            for j in range(4):
                if matrix[i][j] !=  0:
                    newMatrix[i][pos] = matrix[i][j]		
                    pos +=  1	
        return newMatrix		

    def combine(self, matrix):
        for i in range(4):
            for j in range(3):
                if (matrix[i][j] !=  0 and matrix[i][j] ==  matrix[i][j+1]):
                    matrix[i][j] *=  2	
                    matrix[i][j+1] = 0	
                    self.score +=  matrix[i][j]
        return matrix		

    def reverse(self, matrix):
        newMatrix = []		
        for i in range(4):
            newMatrix.append(list(reversed(matrix[i])))		
        return newMatrix		

    def transpose(self, matrix):
        return [list(row) for row in zip(*matrix)]		

    def addNewTile(self):
        row = random.randint(0, 3)		
        col = random.randint(0, 3)		
        while self.matrix[row][col] !=  0:
            row = random.randint(0, 3)		
            col = random.randint(0, 3)		
        self.matrix[row][col] = random.choices([2, 4], [0.9, 0.1])[0]	

    def updateGUI(self):
        for i in range(4):
            for j in range(4):
                cellValue = self.matrix[i][j]		
                if cellValue ==  0:
                    self.cells[i][j]['frame'].configure(bg = c.emptyCellColor)		
                    self.cells[i][j]['number'].configure(bg = c.emptyCellColor, text = '')	
                else:
                    color = c.cellColors.get(cellValue, "#ff0000")		
                    self.cells[i][j]['frame'].configure(bg = color)	
                    self.cells[i][j]['number'].configure(
                        bg = color,
                        fg = c.cellNumberColors.get(cellValue, "#ffffff"),
                        font = c.cellNumberFonts.get(cellValue, ("Helvetica", 40, "bold")),
                        text = str(cellValue))	
        self.scoreLabel.configure(text = self.score)		
        self.update_idletasks()		

    def moveLeft(self, matrix):
        newMatrix = self.stack(matrix)		
        newMatrix = self.combine(newMatrix)		
        newMatrix = self.stack(newMatrix)		
        return newMatrix	

    def moveRight(self, matrix):
        newMatrix = self.reverse(matrix)	
        newMatrix = self.moveLeft(newMatrix)	
        newMatrix = self.reverse(newMatrix)		
        return newMatrix	

    def moveUp(self, matrix):
        newMatrix = self.transpose(matrix)		
        newMatrix = self.moveLeft(newMatrix)		
        newMatrix = self.transpose(newMatrix)		
        return newMatrix	

    def moveDown(self, matrix):
        newMatrix = self.transpose(matrix)		
        newMatrix = self.moveRight(newMatrix)		
        newMatrix = self.transpose(newMatrix)	
        return newMatrix	

    def getValidMoves(self, matrix):
        moves = []	
        for move in ['Left', 'Right', 'Up', 'Down']:
            tempMatrix = copy.deepcopy(matrix)		
            if move ==  'Left':
                movedMatrix = self.moveLeft(tempMatrix)	
            elif move ==  'Right':
                movedMatrix = self.moveRight(tempMatrix)		
            elif move ==  'Up':
                movedMatrix = self.moveUp(tempMatrix)		
            elif move ==  'Down':
                movedMatrix = self.moveDown(tempMatrix)	
            if movedMatrix !=  matrix:
                moves.append(move)	
        return moves		

    def autoPlay(self):
        if self.gameOver():
            return		
        move = ai.getBestMove(self, self.matrix)		
        if move ==  'Left':
            self.matrix = self.moveLeft(self.matrix)	
        elif move ==  'Right':
            self.matrix = self.moveRight(self.matrix)	
        elif move ==  'Up':
            self.matrix = self.moveUp(self.matrix)	
        elif move ==  'Down':
            self.matrix = self.moveDown(self.matrix)	
        self.addNewTile()		
        self.updateGUI()	
        self.recordMove(move)	
        self.after(200, self.autoPlay)	

    def gameOver(self):
        if any(2048 in row for row in self.matrix):
            self.displayGameOver(True)		
            return True		
        if not any(0 in row for row in self.matrix):
            if not self.getValidMoves(self.matrix):
                self.displayGameOver(False)	
                return True	
        return False	

    def displayGameOver(self, won):
        overFrame = tk.Frame(
            self.mainGrid,
            borderwidth = 2)		
        overFrame.place(relx = 0.5, rely = 0.5, anchor = "center")		
        tk.Label(
            overFrame,
            text = "You Win!" if won else "Game Over",
            bg = c.winnerBg if won else c.loserBg,
            fg = c.gameOverFontColor,
            font = c.gameOverFont).pack()	

    def recordMove(self, move):
        self.moveCount +=  1	
        arrowSymbol = ''
        if move ==  'Left':
            arrowSymbol = '←'		
        elif move ==  'Right':
            arrowSymbol = '→'		
        elif move ==  'Up':
            arrowSymbol = '↑'	
        elif move ==  'Down':
            arrowSymbol = '↓'		
        moveLabel = tk.Label(
            self.movesFrameInner,
            text = f"{self.moveCount}. {arrowSymbol}",
            font = ("Helvetica", 14)
        )	
        moveLabel.pack(anchor = 'w')		
        self.moveLabels.append(moveLabel)		
        self.movesList.append(f"{self.moveCount}. {move}")		

    def exportMoves(self):
        filePath = filedialog.asksaveasfilename(
            defaultextension = ".txt", filetypes = [("Text files", "*.txt")])		
        if filePath:
            with open(filePath, 'w') as f:
                for move in self.movesList:
                    f.write(move + '\n')	

if __name__ ==  "__main__":
    Game().mainloop()	