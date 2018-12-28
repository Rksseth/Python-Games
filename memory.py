'''
Memory Game
Apr 26
Cam and Ravi

THINGS TO ADD
-make tkinter gui
-1.when button clicked, sendLocation

'''
import math,random
from tkinter import*
root = Tk()
root.title("Memory")

class Card(object):
    def __init__(self,val0):
        self.x = 0
        self.y = 0
        self.val = val0
        self.visible = 0
        self.g_card = Button(root,text = 'x')
        
class Memory(object):
    def __init__(self):
        self.numCards = 16 #4 ROWS 4 COLUMNS
        self.size = int(math.sqrt(self.numCards))
        
        
        self.mem = [[0 for x in range(self.size)]
                      for y in range(self.size)]
        self.visible = [[0 for x in range(self.size)]
                      for y in range(self.size)]

        self.numPlayers = 2
        self.cardsInv = 25
        self.turns = []

    def isMatchVisible(self,val):
        count = 0
        for row in self.mem:
            for item in row:
                if item.val == val and item.visible:
                    count += 1

        if count == 2:
            return 1
        return 0

    def makeInvisible(self,val):
        for row in range (0,len(self.mem)):
            for col in range(0,len(self.mem[0])):
                if self.mem[row][col].val == val:
                    self.mem[row][col].visible = 0

    def setBoard(self):
        cards = []
        for a in range(0,int(self.numCards/2)):
            for b in range(0,2):
                card = Card(a)
                cards.append(card)

        for row in range (0,len(self.mem)):
            for col in range(0,len(self.mem[0])):
                card = random.choice(cards)
                cards.remove(card)
                self.mem[row][col] = card
                card.x = col
                card.y = row

                card.g_card.place(x = col*50 +10,y = row*50+10)
                card.g_card.config(command=lambda widget=(card.x+card.y/10):self.pTurn(widget))
        return 1
    
    def setNumberPlayers(self):
        numPlay = input("How many Players? ")
        try:
            numPlay = int(numPlay)
        except ValueError:
            print("THATS NOT AN INTEGER")
            return 0
        
        self.numPlayers = numPlay
        return 1

    def printGame(self):
        for row in range (0,len(self.mem)):
            for col in range(0,len(self.mem[0])):
                if self.mem[row][col].visible:
                    #print("%3s" % str(self.mem[row][col].val),end="")
                    self.mem[row][col].g_card.config(text = self.mem[row][col].val)
                    root.update()
                                                     
                else:
                    #print("%3s" %"x",end="")
                    pass
            #print()

    def getTurn(self):
        x = input("X Location: ")
        y = input("Y Location: ")

        try :
            x = int(x)
            y = int(y)
        except ValueError:
            print("NOT AN INT")
            return 0
        if y < self.size and x < self.size and y >= 0 and x >= 0:
            self.mem[y][x].visible = 1
            return self.mem[y][x]
        return 0

    def pTurn(self,loc):
        x = int(loc)
        y = round((loc - int(loc))*10)
        temp = self.mem[y][x]
        #temp = self.getTurn()

        if temp in self.turns:
            return 0
        self.mem[y][x].visible = 1
        self.turns.append(temp)

        
            
        self.printGame()

        if len(self.turns) == 2:
            #CHECK IF THERE IS A MATCH
            correct = self.isMatchVisible(self.turns[0].val)

            if not correct:
                for item in self.turns:
                    self.mem[item.y][item.x].visible = 0
                    root.after(500)
                    self.mem[item.y][item.x].g_card.config(text = 'x')
                    root.update()
                #print("NO MATCH!")
                self.printGame()
                
            else:
                #print("MATCH!")
                for item in self.turns:
                    item.g_card.config(state = DISABLED)
            self.turns = []
        return 1

m = Memory()
m.setBoard()
m.printGame()
        
