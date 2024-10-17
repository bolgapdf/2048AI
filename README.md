# **2048AI**
The classic 2048 game solved in real time with AI using an Expectimax algorithm.

## 📜 Overview

### Features:
- **Graphical User Interface (GUI):** Built with Tkinter, the game displays the AI Agent's attempt at solving the puzzle.
- **Export Move to .txt:** Added ability to export the AI's moves to a .txt file for further analysis.
- **Artificial Intelligence:** AI using an Expectimax Search algorithm to find the most suitable move in an environment that is both known and random.

## 🚀 Getting Started

### Requirements:

	•	Python 3.x
	•	Tkinter Library

### Running the Project:
1.	Clone the repository:
 
```
   git clone https://github.com/bolgapdf/2048AI/
```
2. Import Tkinter:
```
  pip3 install tkinter
```
3. run Command:
```
  python3 2048AI.py
```
## 🤖 AI Algorithm
- Expectimax Search:
  - Player Nodes: the AI explores possible moves (up, down, left, right) and determines which would have the best utility to reach its end goal.
  - Chance Nodes: The AI considers all possible random tiles being added to the board after each move into its decision.
  - Leaf Nodes: When the game reaches a winning/losing state, or a game ending state, it calculates the utility of the game state.

## 🛠️ Challenges and Lessons Learned
- Learning about Expectimax:
  - In my learnings, I have learned about DFS, BFS, Uniform Cost Search, and Minimax functions. I decided against all of these different types of search agents because Expectimax allows my agent to determine utility using both the knowns and the uknowns, and factor both into its final decision.
  - Computational Complexity:
    - While this code is not too demanding, something like this on a larger scale could be dentremental to a computers CPU if not efficently written. I ensured the code is cutting limits to the amound of computations per game state to allow the CPU to maintain proper temperatures and guarentee a smooth delivery.
 - Integrating AI with the GUI:
   - It was difficult determining how to incorporate the AI's moves into the GUI, as my limited experience with AI in games (a pacman search agent) has been purely behind the scenes without a graphical interface.

## ✨ Future Improvements 
  * Corner Strategy:
    * Prioritize keeping the highest tile in a designated corner.
    * Helps organize the board to prevent future hiccups.
    * Done by adding a cost that detures states where the highest tile is not in the corner.
  * Future Tile Merging Potential:
    * Evaluate the potential for a furture merge by analyzing the tiles on board.
    * Encourages AI to create a setup or a "play" to combine tiles in following moves.
    * Analyze the game state and give a greater value to states with the highest potential for a merging tile.
  * Weighted Cell Positions:
    * Assign weights to positions on the board to encourage certain patterns.
    * Allows the AI to create structures/patterns to help solve the puzzle.
    * Created by using a weight matrix corresponding to the tile locations.
