# Minesweeper-Game
Recreated the popular game Minesweeper with additional functionality in Wolfram Mathematica. Additional functions include the ability for the player to create or load a board of any size, play the traditional game, use an AI to solve any board or assist in the game, change game settings, and achieve a high score.

The core AI project was then implemented in Python to test the two following algorithms:
(1) Constraint Satisfaction Problem (CSP) Algorithm
(2) Greedy-Probabilistic (GP) Algorithm

Results: 
The CSP algorithm dominated the GP algorithm. Out of 100 trials, the CSP algorithm on a 10x10 board with a 10% mine density solved the board correctly 96% of the time whereas the GP algorithm solved the board correctly 93% of the time. However, as the mine density increased from 10% to 18%, the CSP solved the board correctly 85% of the time whereas the GP algorithm solved the board correctly only 55% of the time.

The following project was presented at the 2018 Western Kentucky University Mathematics Symposium.
