import math
import copy

def getBestMove(game, matrix):
    depth = 3		
    moves = game.getValidMoves(matrix)	
    if not moves:
        return None		
    scores = []		
    for move in moves:
        tempMatrix = copy.deepcopy(matrix)		
        if move == 'Left':
            tempMatrix = game.moveLeft(tempMatrix)		
        elif move == 'Right':
            tempMatrix = game.moveRight(tempMatrix)
        elif move == 'Up':
            tempMatrix = game.moveUp(tempMatrix)
        elif move == 'Down':
            tempMatrix = game.moveDown(tempMatrix)
        score = expectimax(game, tempMatrix, depth - 1, False)		
        scores.append((score, move))		
    bestScore, bestMove = max(scores, key=lambda x: x[0])		
    return bestMove		

def expectimax(game, matrix, depth, isPlayerTurn):
    if depth == 0 or gameOverState(game, matrix):
        return evaluate(matrix)		

    if isPlayerTurn:
        maxScore = float('-inf')	
        moves = game.getValidMoves(matrix)		
        if not moves:
            return evaluate(matrix)		
        for move in moves:
            tempMatrix = copy.deepcopy(matrix)		
            if move == 'Left':
                tempMatrix = game.moveLeft(tempMatrix)
            elif move == 'Right':
                tempMatrix = game.moveRight(tempMatrix)
            elif move == 'Up':
                tempMatrix = game.moveUp(tempMatrix)
            elif move == 'Down':
                tempMatrix = game.moveDown(tempMatrix)
            score = expectimax(game, tempMatrix, depth - 1, False)	
            maxScore = max(maxScore, score)		
        return maxScore		
    else:
        cells = [(i, j) for i in range(4) for j in range(4) if matrix[i][j] == 0]		
        if not cells:
            return evaluate(matrix)		
        totalScore = 0	
        for value in [2, 4]:
            prob = 0.9 if value == 2 else 0.1		
            for (i, j) in cells:
                tempMatrix = copy.deepcopy(matrix)
                tempMatrix[i][j] = value		
                score = expectimax(game, tempMatrix, depth - 1, True)		
                totalScore += prob * score / len(cells)		
        return totalScore		

def evaluate(matrix):
    emptyCells = sum(row.count(0) for row in matrix)		
    maxTile = max(max(row) for row in matrix)		
    smoothness = calculateSmoothness(matrix)		
    monotonicity = calculateMonotonicity(matrix)	
    return (emptyCells * 1000) + (math.log(maxTile, 2) * 1000) + smoothness + monotonicity	

def calculateSmoothness(matrix):
    smoothness = 0	
    for i in range(4):
        for j in range(3):
            if matrix[i][j] != 0 and matrix[i][j+1] != 0:
                smoothness -= abs(matrix[i][j] - matrix[i][j+1])		
    for j in range(4):
        for i in range(3):
            if matrix[i][j] != 0 and matrix[i+1][j] != 0:
                smoothness -= abs(matrix[i][j] - matrix[i+1][j])	
    return smoothness		

def calculateMonotonicity(matrix):
    totals = [0, 0, 0, 0]	
    for i in range(4):
        current = 0
        next = current + 1
        while next < 4:
            while next < 4 and matrix[i][next] == 0:
                next += 1
            if next >= 4:
                break
            currentValue = math.log(matrix[i][current], 2) if matrix[i][current] != 0 else 0	
            nextValue = math.log(matrix[i][next], 2) if matrix[i][next] != 0 else 0		
            if currentValue > nextValue:
                totals[0] += nextValue - currentValue	
            elif currentValue < nextValue:
                totals[1] += currentValue - nextValue		
            current = next
            next += 1
    for j in range(4):
        current = 0
        next = current + 1
        while next < 4:
            while next < 4 and matrix[next][j] == 0:
                next += 1
            if next >= 4:
                break
            currentValue = math.log(matrix[current][j], 2) if matrix[current][j] != 0 else 0
            nextValue = math.log(matrix[next][j], 2) if matrix[next][j] != 0 else 0
            if currentValue > nextValue:
                totals[2] += nextValue - currentValue	
            elif currentValue < nextValue:
                totals[3] += currentValue - nextValue	
            current = next
            next += 1
    return max(totals[0], totals[1]) + max(totals[2], totals[3])		

def gameOverState(game, matrix):
    if any(2048 in row for row in matrix):
        return True		
    if not any(0 in row for row in matrix):
        if not game.getValidMoves(matrix):
            return True	
    return False		