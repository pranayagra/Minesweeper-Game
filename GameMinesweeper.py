import numpy as np
np.set_printoptions(threshold=np.nan)
from tkinter import *
from functools import partial
from itertools import product
from scipy.optimize import minimize
from scipy.optimize import lsq_linear
import random


# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)
class Window(Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        
        # parameters that you want to send through the Frame class. 
        Frame.__init__(self, master)   

        #reference to the master widget, which is the tk window                 
        self.master = master

        #with that, we want to then run init_window, which doesn't yet exist
        global numRows
        global numCols
        global outcome
        global numBombs
        global terminate
        outcome = 0

        terminate = False
        #AI 1
        global matrixOne
        global vectorSolutions
        global definiteBombs

        #AI 2
        global probsList
        global permanentBombsList
        global permanentNotBombsList



        numRows = int(input("# of Rows: "))
        numCols = int(input("# of Cols: "))
        numBombs = int(input("# of Bombs: "))

        matrixOne = np.empty((0,numRows*numCols), int)
        
        permanentBombsList = np.full((numRows,numCols), 0)
        permanentNotBombsList = np.full((numRows,numCols), 0)

        self.init_window()

    #Creation of init_window
    def init_window(self):
        # print(x, y)
        # changing the title of our master widget      
        self.master.title("Minesweeper")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a button instance
        #quitButton = Button(self, text="Exit",command=self.client_exit)

        # placing the button on my window
        #quitButton.place(x=0, y=0)
        
        for row in range(0, numRows):
            curRow = []
            for col in range(0, numCols):
                #curRow.append(Button(self, bg="gray", width=2,height=1, command=lambda: self.open_button(row, col)))
                curRow.append(Button(self, bg="gray", width=2,height=1, command=lambda rw=row, cl=col: self.open_button(rw, cl)))
                curRow[col].grid(row=row,column=col)
            but.append(curRow)

        self.generate_board()
        CSPButton = Button(self, bg="blue", text="CSP", width=6, height=5, command=self.AICSP)
        CSPButton.place(x=600,y=150)

        AIButton = Button(self, bg="blue", text="Greedy", width=6, height=5, command=self.AIProbs)
        AIButton.place(x=600,y=350)

    def open_button(self, r, c):
        global outcome
        global numBombs
        global terminate

        but[r][c].config(state="disabled")
        if(ans[r][c]!=-100):
            but[r][c]["text"] = ans[r][c]
            but[r][c]["bg"] = "white"
        else:
            but[r][c]["bg"] = "red"
            if(outcome == 0):
                outcome = -1

        if(ans[r][c] == 0):
            self.open_board(r, c)

        if(self.gameWon() == numBombs and outcome == 0):
            outcome = 1

        if(outcome==-1 or outcome ==1):
            #write to file (won or loss)
            #root.destroy()
            terminate = True
            if(outcome==1):
                print("WIN")
            else:
                print("LOSS")

    def gameWon(self):
        cnt = 0
        for row in range(0, numRows):
            for col in range(0, numCols):
                if(but[row][col]['state'] != 'disabled'):
                    cnt = cnt+1
        return cnt

    def open_board(self, r, c):
        if(r>=0 and c>=0 and r<numRows and c<numCols):
            but[r][c].config(state="disabled")
            but[r][c]["text"] = ""
            but[r][c]["bg"] = "white"
        for i in range(-1, 2):
            for j in range(-1, 2):
                self.open_OneMoreTime(r + i, c + j)

    def open_OneMoreTime(self, rXtra, cXtra):
        if(rXtra>=0 and cXtra>=0 and rXtra<numRows and cXtra<numCols):
            if(but[rXtra][cXtra]['state'] != 'disabled'):
                but[rXtra][cXtra].config(state="disabled")
                if(ans[rXtra][cXtra] == 0):
                    self.open_board(rXtra, cXtra)
                else:
                    but[rXtra][cXtra]["text"] = ans[rXtra][cXtra]
                    but[rXtra][cXtra]["bg"] = "white"
                    # add statement to call add matrix for CSP Problem...            



    def generate_board(self):
        global numBombs
        global ans

        bombList = []
        bombsNotAllowed = []
        for tX in range(-1, 2):
            for tY in range(-1, 2):
                bombsNotAllowed.append([numRows//2+tX, numCols//2+tY])
        ans = np.full((numRows,numCols), 0)

        while len(bombList) < numBombs:
            tempX = random.randint(0, numRows-1)
            tempY = random.randint(0, numCols-1)
            if( [tempX, tempY] not in bombList and [tempX, tempY] not in bombsNotAllowed):
                bombList.append([tempX, tempY])
                ans[tempX][tempY] = -100



        for row in range(0, numRows):
            for col in range(0, numCols):
                if ans[row][col] == 0:
                    temp = 0
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            currCheckrow = row+i
                            currCheckcol = col+j
                            if(currCheckrow>= 0 and currCheckcol>=0 and currCheckrow<numRows and currCheckcol<numCols):
                                if ans[row+i][col+j] == -100:
                                    temp += 1   
                    ans[row][col] = temp


    def AICSP(self):
        #A CSP approach to the problem... empty board, make first move.
        global matrixOne
        global vectorSolutions
        global next_Button_Open
        global vectorSolutions
        global outcome
        global terminate



        if(self.newBoard() == True):
            vectorSolutions = np.array([])
            self.open_button(numRows//2, numCols//2)
            #set up matrix for first time...
            for row in range(0, numRows):
                for col in range(0, numCols):
                    if(but[row][col]['state'] == 'disabled' and but[row][col]["text"] != ""): #a button that is opened and is not useless (numbered) 
                        vectorSolutions = np.append(vectorSolutions, [int(but[row][col]["text"])])
                        temp = np.zeros(numRows*numCols)
                        temp = self.add_3by3_constraint(temp, row, col)
                        matrixOne = np.append(matrixOne, np.array([temp]), axis=0)
            myAns = lsq_linear(matrixOne, vectorSolutions, bounds=(-0.0000, 1.0001)).x
            myAns = np.reshape(myAns, (numRows, numCols))
            next_Button_Open = self.findCurrMin(myAns)
            but[next_Button_Open[0][0]][next_Button_Open[0][1]]["bg"] = "blue" 
        #append... solve... display... find min/solve... click...
        # click...
        else:
            self.open_button(next_Button_Open[0][0], next_Button_Open[0][1])
            if(terminate == True):
                return
            for row in range(0, numRows):
                for col in range(0, numCols):
                    if(but[row][col]['state'] == 'disabled' and but[row][col]["text"] != ""): 
                        vectorSolutions = np.append(vectorSolutions, [int(but[row][col]["text"])])
                        temp = np.zeros(numRows*numCols)
                        temp = self.add_3by3_constraint(temp, row, col)
                        matrixOne = np.append(matrixOne, np.array([temp]), axis=0)
            myAns = lsq_linear(matrixOne, vectorSolutions, bounds=(-0.0000, 1.0001)).x
            myAns = np.reshape(myAns, (numRows, numCols))
            next_Button_Open = self.findCurrMin(myAns)
            if(next_Button_Open == [-1,-1]):
                next_Button_Open = self.moveLeftIssue(myAns)
            but[next_Button_Open[0][0]][next_Button_Open[0][1]]["bg"] = "blue" 


    def moveLeftIssue(self, myAns):
        for row in range(0, numRows):
            for col in range(0, numCols):
                if(but[row][col]['state'] != 'disabled' and round(myAns[row][col], 1) != 1):
                    return [[row, col]]


    def findCurrMin(self, myAns):
        cMIN = 1
        index = [-1, -1]
        for row in range(0, numRows):
            for col in range(0, numCols):
                if(but[row][col]['state'] != 'disabled'): #clickable
                    if(myAns[row][col] > 0 and self.isTouching(row, col)):
                        but[row][col]["text"] = round(myAns[row][col], 1)
                        if(cMIN > round(myAns[row][col], 2)):
                            cMIN = round(myAns[row][col], 2)
                            index = [[row, col]]
        return index


    def printProbs(self, myAns):
        for row in range(0, numRows):
            for col in range(0, numCols):
                if(but[row][col]['state'] != 'disabled'): #clickable
                    if(self.isTouching(row, col)):
                        but[row][col]["text"] = round(1.0 - round(myAns[row][col], 1), 1)


    def isTouching(self, r, c):
        for i in range(-1, 2):
            for j in range (-1, 2):
                if(r+i>=0 and c+j>=0 and r+i<numRows and c+j<numCols):
                    if(but[r+i][c+j]['state'] == 'disabled'):
                        return True
        return False


    def add_3by3_constraint(self, temp, r, c):
        #print(r, ", ", c)
        for i in range(-1, 2):
            for j in range(-1, 2):
                if(r+i>=0 and c+j>=0 and r+i<numRows and c+j<numCols):
                    #valid buttons
                    #print((r+i), ", ", (c+j))
                    if(but[r+i][c+j]['state'] != 'disabled'): #mystery square...
                        temp[numCols*(r+i) + (c+j)] = 1
        return temp


    def newBoard(self):
        for row in range(0, numRows):
            for col in range(0, numCols):
                if(but[row][col]['state'] == 'disabled'):
                    #print("False")
                    return False
        #print("True")
        return True


    #AI 2 using a probablistitc approach
    def AIProbs(self):
        
        #DELETE BELOW IF FAILED
        global permanentBombsList
        global maxProbs
        global maxProbsCoords
        global probsList
        global localNotBombsList
        global localBombsList
        maxProbs = 0
        maxProbsCoords = []
        #DELETE ABOVE IF FAILED


        if(self.newBoard() == True):
            self.open_button(numRows//2, numCols//2)
        else:
            if(len(localBombsList) == 0 and len(localNotBombsList) == 0): #must choose highest probability...
                #maxProbs = 0
                #maxProbsCoords = []
                for row in range(0, numRows):
                    for col in range(0, numCols):
                        if(maxProbs < probsList[row][col] and probsList[row][col] < 1):
                            maxProbs = probsList[row][col]
                            maxProbsCoords = [[row, col]]
                if(terminate == True):
                        return
                #print(maxProbsCoords)
                if(maxProbsCoords == []):
                    maxProbsCoords = self.moveLeftIssue(probsList)
                    #print(maxProbsCoords)
                if(but[maxProbsCoords[0][0]][maxProbsCoords[0][1]]['state'] != 'disabled'):
                    self.open_button(maxProbsCoords[0][0], maxProbsCoords[0][1])
                    if(terminate == True):
                        return
            elif(len(localNotBombsList)>0):
                for i in range(0, len(localNotBombsList)):
                    if(but[localNotBombsList[i][0]][localNotBombsList[i][1]]["text"] != 'disabled'):
                        self.open_button(localNotBombsList[i][0], localNotBombsList[i][1])
                        if(terminate == True):
                            return
                localNotBombsList = []
 
        probsList = np.full((numRows, numCols), 1.0)
       
        for row in range(0, numRows):
            for col in range(0, numCols):
                if(permanentBombsList[row][col] == 1):
                    probsList[row][col] = 0.0

        localBombsList = []
        localNotBombsList = []

        for row in range(0, numRows):
            for col in range(0, numCols):

                surround3x3 = []
                buttons3x3 = []
                definiteBombs3x3 = []
                definiteNotBombs3x3 = []
                unsureButtons3x3 = []

                if(but[row][col]['state'] == 'disabled' and but[row][col]["text"] != ""):
                    for surrR in range(-1, 2):
                        for surrC in range(-1, 2):
                            if(row+surrR>=0 and col+surrC>=0 and row+surrR<numRows and col+surrC<numCols):
                                surround3x3.append([row+surrR, col+surrC])
                                if(but[row+surrR][col+surrC]['state'] != 'disabled'):
                                    buttons3x3.append([row+surrR, col+surrC])
                                    if(permanentBombsList[row+surrR][col+surrC] == 1):
                                        definiteBombs3x3.append([row+surrR, col+surrC])
                                    if(permanentNotBombsList[row+surrR][col+surrC] == 1):
                                        definiteNotBombs3x3.append([row+surrR, col+surrC])
                                    if(permanentBombsList[row+surrR][col+surrC] != 1 and permanentNotBombsList[row+surrR][col+surrC] != 1):
                                        unsureButtons3x3.append([row+surrR, col+surrC])
                    
                    numerator = int(but[row][col]["text"]) - len(definiteBombs3x3)
                    denomenator = len(unsureButtons3x3)
                    if(denomenator != 0):
                        fracProb = 1 - numerator/denomenator
                        for unusedCnts in range(0, denomenator):
                            tempCoord = unsureButtons3x3[unusedCnts]
                            PLCurr = probsList[tempCoord[0]][tempCoord[1]] * fracProb
                            probsList[tempCoord[0]][tempCoord[1]] = PLCurr
                            if(permanentNotBombsList[tempCoord[0]][tempCoord[1]] == 1):
                                probsList[tempCoord[0]][tempCoord[1]] = 1
                            if(fracProb == 0):
                                permanentBombsList[tempCoord[0]][tempCoord[1]] = 1
                                localBombsList.append(tempCoord)
                            if(fracProb == 1):
                                permanentNotBombsList[tempCoord[0]][tempCoord[1]] = 1
                                localNotBombsList.append(tempCoord)
                                probsList[tempCoord[0]][tempCoord[1]] = 1
                    #print("pL: ", probsList)
                    #self.findCurrMin(probsList)
        self.printProbs(probsList)


# root window created. Here, that would be the only window, but
# you can later have windows within windows.
root = Tk()
but = []
ans = []
root.geometry("800x800")
#creation of an instance
app = Window(root)

#mainloop 
root.mainloop()