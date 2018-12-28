'''
Ravi Seth and a bit of Raveena D'Souza and a tiny bit of Bjarne Lahrsen
May 16
'''
import math,copy
from tkinter import*
from tkinter import font

root = Tk()
root.configure(background = 'grey70')
root.title("Chess")

class Piece(object):
    def __init__(self,name0):
        self.name = name0
        self.x = 0
        self.y = 0
        self.directions = []
        self.canMultiply = 0

        self.isRed = 0

#KING
KING = Piece("K")
KING.directions.append(math.sqrt(2))
KING.directions.append(1)
KING.canMultiply = 0

#QUEEN
QUEEN = Piece("Q")
QUEEN.directions.append(math.sqrt(2))
QUEEN.directions.append(1)
QUEEN.canMultiply = 1

#BISHOP
BISH = Piece("B")
BISH.directions.append(math.sqrt(2))
BISH.canMultiply = 1

#HORSE
HORSE = Piece("H")
HORSE.directions.append(math.sqrt(5))
HORSE.canMultiply = 0

#ROOK
ROOK = Piece("R")
ROOK.directions.append(1)
ROOK.canMultiply = 1

#PAWN
PAWN = Piece("P")
PAWN.directions.append(1)
PAWN.directions.append(math.sqrt(2))
PAWN.canMultiply = 1

BASE_ROW = [ROOK,HORSE,BISH,QUEEN,KING,BISH,HORSE,ROOK]

class Chess(object):
    def __init__(self):
        self.dim = 8
        self.cap = self.dim*self.dim

        self.grid = [[0 for x in range(0,self.dim)] for y in range(0,self.dim)]

        self.turn = 1
        
        #self.avail_moves = []

        self.move = 0

        self.check = 0

        root.geometry(str((self.dim+1)*30)+'x'+str((self.dim+1)*30))

    def setup(self):
        #SETUP BLACK MAYJOR AND MINOR PIECES
        row = 0
        for col in range(0,self.dim):
            temp = copy.copy(BASE_ROW[col])
            temp.x = col
            temp.y = row
            temp.isRed = 0
            self.grid[row][col] = temp

        
        #SETUP BLACK INFANTRY
        row = 1
        for col in range(0,self.dim):
            temp = copy.copy(PAWN)
            temp.x = col
            temp.y = row
            temp.isRed = 0
            self.grid[row][col] = temp
            
        #SETUP WHITE MAJOR AND MINOR PIECES
        row = self.dim - 1
        for col in range(0,self.dim):
            temp = copy.copy(BASE_ROW[col])
            temp.x = col
            temp.y = row
            temp.isRed = 1
            self.grid[row][col] = temp
        
        #SETUP WHITE INFANTRY
        row = self.dim - 2
        for col in range(0,self.dim):
            temp = copy.copy(PAWN)
            temp.x = col
            temp.y = row
            temp.isRed = 1
            self.grid[row][col] = temp
        
    def cout(self):
        
        #print("  ",end=" ")
        for col in range(0,self.dim):
            #print(col,end="  ")
            l = Label(text = col,fg = 'black',bg = 'grey70').place(x =col*30+30, y = 0)
        #print()
        
        
        for row in range(0,self.dim):
            #print(row,end= " ")
            l = Label(text = row,fg = 'black',bg = 'grey70').place(x = 0,y  =row*30+30)
            for col in range(0,self.dim):
                item = self.grid[row][col]
                text = ""
                fg = ""

                if (row % 2 == 0 and col % 2 == 0) or not (row % 2 == 0 or col % 2 == 0):
                    bg = 'PeachPuff2'
                elif (row % 2 is not 0 and col % 2 == 0) or (col % 2 is not 0 and row % 2 == 0):
                    bg = 'medium aquamarine'
                    
                
                
                if item:
                    #JUST TO MAKE SURE
                    item.x = col
                    item.y = row
                    
                    if item.isRed:
                        text += "R"
                        fg = "white"
                    else:
                        text += "B"
                        fg = "black"
                    text += item.name
                else:
                    text = ". "
                    fg = 'white'

                #print(text,end = " ")

                l = Label(root,text = text[1],width = 2,fg= fg,bg=bg)
                l.place(x = 30*col+30,y = 30*row+30)

            #print()
        #print()

        return 1

    def validIdx(self,x,y):
        if x>=0 and x< self.dim and y>=0 and y<self.dim:
            return True

        return False

    def getTurn(self):

        x = input("x : ")

        y = input("y : ")



        try:

            x = int(x)

            y = int(y)

            return x,y

        except ValueError:  

            print("NOT AN INT")

            return -1,-1

    def getDirections(self,piece):
        if not piece:
            return []
        avail_moves = []
        for x in range(0,self.dim):
            for y in range(0,self.dim):
                if x == piece.x and y == piece.y:
                    pass
                else:
                    dx = piece.x - x
                    dy = piece.y -y
                    rad = math.sqrt(math.pow(dx,2) + math.pow(dy,2))
                    if piece.canMultiply:
                        valid = self.validMove(piece,x,y)
                        if valid:
                            avail_moves.append((x,y))

                    if not piece.canMultiply and rad in piece.directions:
                        avail_moves.append((x,y))

                        
        #FILTER self.avail_moves
        temp = []
        for item in avail_moves:
            blocked = self.moveBlocked(piece,item[0],item[1])
            if not blocked:
                temp.append(item)
        avail_moves = temp

        #if a PAWN, do a PAWN FILTER
        if piece.name == "P":
            avail_moves = self.pawnFilter(piece,avail_moves)

        return avail_moves

    def moves(self):
        allDirections = {}
        for row in range(0,self.dim):
            for col in range(0,self.dim):
                piece = self.grid[row][col]
                if piece:
                    avail_moves = self.getDirections(piece)

                    if len(avail_moves) > 0:
                        allDirections[piece] = avail_moves
        return allDirections
                
    def movePiece(self,x,y):
        if not self.validIdx(x,y):
            return []

        try:
            if self.grid[y][x] and (self.grid[y][x].isRed and self.turn) or (not self.grid[y][x].isRed and not self.turn):
                #THIS IS A SELECTED PIECE
                text = ""
                if self.grid[y][x].isRed:
                    text = "R"
                else:
                    text = "B"
                #print('PIECE DETECTED ->', text+self.grid[y][x].name)
                self.move = self.grid[y][x]
                return 1
            else:
                x = self.locDetected(x,y)
                if x:
                    #print("APPROVED")
                    pass
                else:
                    #print("DENIED")
                    pass
                return x

        except:
            x = self.locDetected(x,y)
            if x:
                #print("APPROVED")
                pass
            else:
                #print("DENIED")
                pass
            return x
        return 0

    def locDetected(self,x,y):
        if not self.move:
            return 0
        #LOCATION SELECTED IS AN OPEN SPOT OR A SPOT TO TAKE
        #print("LOCATION DETECTED")
        avail_moves = []
        
        #avail_moves = self.getDirections(self.move)
        allDirections = self.moves()
        if self.move in allDirections:
            avail_moves = allDirections[self.move]
        else:
            return 0

        #print(avail_moves)

        if self.inCheck():
            SOS = self.inMate()
            if self.move in SOS:
                avail_moves = SOS[self.move]
            else:
                return 0
        print(self.move.name,avail_moves)
        
        if len(avail_moves) == 0:
            return 0
        if (x,y) in avail_moves:
            tempPiece = copy.copy(self.move)
            tempGrid = copy.copy(self.grid)
            
            #MOVE PIECE TO SPOT            
            origX = tempPiece.x
            origY = tempPiece.y
            
            tempPiece.y = y
            tempPiece.x = x
            self.grid[y][x] = tempPiece
            self.grid[origY][origX] = 0


            #upgrade PAWN?
            if tempPiece.name == "P":
                self.upgradePAWN(tempPiece)

            #FROM BEFORE-----------------------
            '''
            pieceInCheck  = self.inCheck()

            if pieceInCheck:
                print("CHECK on", (pieceInCheck.x,pieceInCheck.y),"by", (tempPiece.x,tempPiece.y))
            try:
                #THE OTHER KING IS IN CHECK - VALID
                if (pieceInCheck.isRed and not self.turn) or (not pieceInCheck.isRed and self.turn):
                    
                    self.move = 0
                    self.turn =  not self.turn
                    avail_moves = []

                #THE SAME KING IS IN CHECK - INVALID
                elif (pieceInCheck.isRed and self.turn) or (not pieceInCheck.isRed and not self.turn):
                    #print("IN CHECK , YUH HERE")
                    self.grid[tempPiece.y][tempPiece.x] = 0
                    self.grid[self.move.y][self.move.x] = self.move
                    return 0

            #NO PIECE IN CHECK - VALID
            except:
                
                self.move = 0
                self.turn =  not self.turn
                avail_moves = []
            '''
            #---------------------------------
    
            
            self.move = 0
            self.turn =  not self.turn
            avail_moves = []
            return 1
        return 0

    def validMove(self,piece,x1,y1):
        interMoves = []
        for x in range(x1-1,x1+2):
            for y in range(y1-1,y1+2):
                if self.validIdx(x,y) and x is not x1 or y is not y1:
                    dx = (x1-x)
                    dy = (y1-y)
                    rad = math.sqrt(math.pow(dx,2) + math.pow(dy,2))
                    
                    if rad in piece.directions:
                        interMoves.append((dx,dy))
        dx_test = (piece.x-x1)
        dy_test = (piece.y-y1)
        for item in interMoves:
            try:
                factor = dx_test / item[0]
                if item[1] * factor == dy_test:
                    return 1
            except:
                #DX is zero
                if item[0] == dx_test:
                    return 1
        return 0

    def moveBlocked(self,piece,x1,y1):
        try:
            if piece.isRed == self.grid[y1][x1].isRed:
                #BLOCKED BY OWN PIECE AT END POSITION
                #print("BLOCKED AT", x1,y1)
                return 1
            elif piece.name == "P" and self.grid[y1][x1] and piece.x == x1:
                return 1
        except:
            pass
        
        if piece.name == "H":
            return 0
        
        
        dx = x1 - piece.x
        dy = y1 - piece.y

        ux = 0
        uy = 0
        try:
            ux = round(dx/abs(dx))
        except:
            ux = 0
        try:
            uy = round(dy/abs(dy))
        except:
            uy = 0

        interX = piece.x
        interY = piece.y
        while interX is not x1 or interY is not y1:
            interX += ux
            interY += uy

            if not self.validIdx(interX,interY):
                return 1
            try:

                #IF IT IS BLOCKED A PIECE BEFORE THE END
                if not(interX == x1 and interY == y1) and self.grid[interY][interX] :
                    #BLOCKED
                    #print("BLOCKED AT", x1,y1)
                    return 1
                elif interX == x1 and interY == y1 and self.grid[interY][interX].isRed is not piece.isRed :
                    return 0
                
                    
            except:
                #IT IS AN OPEN SPOT
                pass
        return 0

    def pawnFilter(self,piece,avail_moves):
        if not piece:
            return avail_moves
        '''
        ASSUMING this function is called in a PAWN piece, this function will PERFORM the follwoing

        *Note : self.AVAIL_MOVES only has moves that the PAWN CAN move, NOTHING BLOCKED

        it will filter the following out of self.AVAIL_MOVES :
            - remove any moves that go backwards
            - only move a single root(2) if it is a take
            - only move a double foreward up 2 if still on the same row as the begining

            -moves only going 1 foreward are ok
        '''
        temp = []
        for item in avail_moves:
            dx = item[0] - piece.x
            dy = item[1] - piece.y
            rad = math.sqrt(math.pow(dx,2) + math.pow(dy,2))
            if (piece.isRed and dy < 0) or (not piece.isRed and dy > 0):
                #PAWN moving FOREWARD
                if rad == 2 and ((piece.y == 1 and not piece.isRed) or (piece.y == self.dim - 2 and piece.isRed)):
                    #VALID MOVE up 2
                    #print("added",item)
                    temp.append(item)

                if rad == 1:
                    #VALID MOVE up 1
                    #print("aadded",item)
                    temp.append(item)

                try:
                    tempItem = self.grid[item[1]][item[0]]
                    
                    if rad == math.sqrt(2) and tempItem and ((tempItem.isRed and not self.turn) or (not tempItem.isRed and self.turn)):
                        #print("aaadded",item,rad)
                        temp.append(item)
                except:
                    pass
        avail_moves = temp
        return avail_moves

    def upgradePAWN(self,piece):
        if (piece.isRed and piece.y == 0) or (not piece.isRed and piece.y == self.dim - 1):
            temp = copy.copy(QUEEN)
            temp.x = piece.x
            temp.y = piece.y

            self.grid[piece.y][piece.x] = temp

            return 1
        return 0

    def inCheck(self):
        for row in self.grid:
            for item in row:
                if item:
                    
                    avail_moves = self.getDirections(item)
                    
                    for d in avail_moves:
                        king = self.grid[d[1]][d[0]]
                        if king:
                            if king.name == "K" and king.isRed is not item.isRed:
                                #print("CHECK on", d ,'by' ,(item.x,item.y))
                                avail_moves = []
                                return king
        avail_moves = []
        return 0

    def inMate(self):
        SOS = {}
        
        KING_check = self.inCheck()
        if KING_check:
            print("CHECK on",(KING_check.x,KING_check.y))
        if not KING_check:
            return {}

        temporary = copy.copy(self.grid)
        for row in range(0,self.dim):
            for col in range(0,self.dim):
                piece = temporary[row][col]
                
                
                if piece:
                    if piece.isRed is KING_check.isRed:

                        avail_moves = self.getDirections(copy.copy(piece))

                        for d in avail_moves:
                            x = d[0]
                            y = d[1]

                            slotPiece = copy.copy(self.grid[y][x])

                            #MOVE PIECE
                            self.grid[piece.y][piece.x] = 0
                            tempPiece = copy.copy(piece)
                            tempSlot = copy.copy(self.grid[y][x])
                            tempPiece.x = x
                            tempPiece.y = y

                            self.grid[y][x] = tempPiece

                            pieceInCheck = self.inCheck()

                            try:
                                if not pieceInCheck or KING_check.isRed is not pieceInCheck.isRed:

                                    if slotPiece:
                                        slotPiece.x = x
                                        slotPiece.y = y
                                    
                                    self.grid[y][x] = slotPiece

                                    piece.x = col
                                    piece.y = row
                                    self.grid[row][col] = piece

                                    if piece in SOS:
                                        SOS[piece].append(d)
                                    else:
                                        SOS[piece] = [d]
                                    #return 0
                            except:
                                pass



                            if slotPiece:
                                slotPiece.x = x
                                slotPiece.y = y
                            
                            self.grid[y][x] = slotPiece

                            piece.x = col
                            piece.y = row
                            self.grid[row][col] = piece
        
        if not SOS:
            print("MATE")
        return SOS
                        

                
        
            
    

c = Chess()
c.setup()
'''
temp = copy.copy(HORSE)
temp.isRed = 0
c.grid[0][0] = temp


temp2 = copy.copy(ROOK)
temp2.isRed = 1
temp2.x= 0
temp2.y = 6


c.grid[6][0] = temp2


c.cout()

'''
#Check Mate 1
'''
c.movePiece(5,6)
c.movePiece(5,5)

c.movePiece(4,1)
c.movePiece(4,2)

c.movePiece(6,6)
c.movePiece(6,4)

c.movePiece(3,0)
c.movePiece(7,4)
'''



#Check Mate 2
'''
c.movePiece(3,6)
c.movePiece(3,4)

c.movePiece(1,1)
c.movePiece(1,3)

c.movePiece(2,6)
c.movePiece(2,4)

c.movePiece(1,3)
c.movePiece(1,4)

c.movePiece(3,4)
c.movePiece(3,3)

c.movePiece(6,0)
c.movePiece(5,2)

c.movePiece(1,7)
c.movePiece(2,5)

c.movePiece(5,2)
c.movePiece(3,3)

c.movePiece(2,5)
c.movePiece(3,3)

c.movePiece(6,1)
c.movePiece(6,3)

c.movePiece(3,3)
c.movePiece(2,1)

c.movePiece(3,0)
c.movePiece(2,1)

c.movePiece(2,7)
c.movePiece(6,3)

c.movePiece(2,1)
c.movePiece(2,4)

c.movePiece(4,6)
c.movePiece(4,4)

c.movePiece(2,4)
c.movePiece(4,4)

c.movePiece(3,7)
c.movePiece(4,6)

c.movePiece(4,4)
c.movePiece(4,6)

c.movePiece(5,7)
c.movePiece(4,6)

c.movePiece(5,0)
c.movePiece(7,2)

c.movePiece(6,3)
c.movePiece(7,2)

c.movePiece(2,0)
c.movePiece(0,2)

c.movePiece(6,7)
c.movePiece(5,5)

c.movePiece(0,2)
c.movePiece(4,6)

c.movePiece(4,7)
c.movePiece(4,6)

c.movePiece(1,4)
c.movePiece(1,5)

c.movePiece(0,6)
c.movePiece(1,5)

c.movePiece(0,1)
c.movePiece(0,2)

c.movePiece(0,7)
c.movePiece(0,2)

c.movePiece(1,0)
c.movePiece(2,2)

c.movePiece(0,2)
c.movePiece(0,0)

c.movePiece(2,2)
c.movePiece(1,0)

c.movePiece(0,0)
c.movePiece(1,0)
'''

c.cout()

count = 0

while True:
    if c.inCheck():
        SOS = c.inMate()
        if not SOS:
            break
    root.update()
    count += 1

    if not c.turn:
        print("Black Turn")
    else:
        print("Red Turn")
    
    x,y = c.getTurn()
    c.movePiece(x,y)

    if not c.move:
        c.cout()

    



    
