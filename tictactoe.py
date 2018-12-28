'''
TIC TAC TOE
MAY 5
'''
from tkinter import*
root = Tk()

class piece(object):
    def __init__(self,letter0,x,y):
        self.x = x
        self.y = y
        self.letter = letter0


class game(object):
    def __init__(self):
        self.slots = 3
        self.b = [[0 for x in range(0,self.slots)] for y in range(0,self.slots)]
        self.turn = 0
        self.used = 0
        root.geometry(str(self.slots*30)+'x'+str(self.slots*30))

    def validIdx(self,x,y):
        if x>=0 and x<self.slots and y>=0 and y<self.slots:
            return True
        return False
    
    def checkBoard(self):
        #CHECK ROWS
        for row in self.b:
            word = ""
            for item in row:
                if item:
                    word = word+item.letter
                else:
                    word = word+" "
            if 'XXX' in word or 'OOO' in word:
                print('WINNER')
                return True

        #CHECK COLUMNS
        for col in range(0,self.slots):
            word = ""
            for row in range(0,self.slots):
                if self.b[row][col]:
                    word = word+self.b[row][col].letter
                else:
                    word = word+" "
            if 'XXX' in word or 'OOO' in word:
                print('WINNER')
                return True
        #CHECK DIAGONALS
        dx = 1
        dy = 1
        for row in range(0,self.slots,self.slots-1):
            for col in range(0,self.slots,self.slots-1):
                win = self.diag(col,row,dx,dy)
                if win:
                    print("WINNER")
                    return True
                dx *= -1
                
            dy *= -1
            
        return False

    def diag(self,x,y,dx,dy):
        if not self.validIdx(x,y):
            return False
        word = ""
        temp_x = x
        temp_y = y
        while(self.validIdx(temp_x,temp_y)):
            if self.b[temp_y][temp_x]:
                word = word+self.b[temp_y][temp_x].letter
            else:
                word = word+" "
            temp_x += dx
            temp_y += dy
        if 'XXX' in word or 'OOO' in word:
            return True

        x = self.diag(x+1,y,dx,dy)
        y = self.diag(x,y+1,dx,dy)

        if x or y:
            return True
        return False

    def addPiece(self,x,y):
        if self.validIdx(x,y):
            if not self.b[y][x]:
                self.turn = not self.turn
                letter = ""
                if self.turn:
                    letter = 'X'

                else:
                    letter = 'O'
                self.b[y][x] = piece(letter,x,y)
                self.used+= 1
                self.printBoard()
                self.checkBoard()
                return True
        return False

    def inputAddPiece(self):
        x = int(input('x: '))
        y = int(input('y: '))

        self.addPiece(x,y)

    def convertAddPiece(self,num):
        x = int(num)
        y = round((num - x)*10)
        self.addPiece(x,y)

    def printBoard(self):
        for y in range(0,self.slots):
            for x in range(0,self.slots):
                text = "_"
                if self.b[y][x]:
                    #print(self.b[y][x].letter,end=' ')
                    text = self.b[y][x].letter
                else:
                    #print("_",end=" ")
                    pass
                l = Button(root,text=" "+text+" ",command = lambda widget=(x+y/10):self.convertAddPiece(widget),bg = 'dark salmon',fg='black')
                l.place(x= x*30,y= y*30)
            #print()
        #print()
                
g = game()
g.printBoard()
win = False
'''
while(g.used < g.slots*g.slots or not win):
    g.inputAddPiece()
    g.printBoard()
    win = g.checkBoard()
    if win:
        break
    '''
 
