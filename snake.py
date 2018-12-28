'''
Ravi Seth
May 5
'''
from tkinter import*
import random
root = Tk()
root.title("Sneek Sneke Snake Snack Shack Snooke Snaka Shook Shake Yack Yip Self Swell Sweat Swealt Smealth Smealt")
c = Canvas(root)

class Node(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.next = 0
        self.prev = 0
        self.l = Label(root,text = "~",bg = 'green',fg='white',width =2)
        

class LinkedList(object):
    def __init__(self):
        self.head = 0
        self.length = 20
        self.grid = [[0 for x in range(0,self.length)] for y in range(0,self.length)]
        
        root.geometry(str(self.length*30)+'x'+str(self.length*30))
        self.size = 0
        self.dx = 0
        self.dy = 0
        self.curBall = 0

        self.addNode()
    def left(self,event):
        self.shiftLR(-1)
        self.dx = -1
        self.dy = 0
        self.collision()
        return True
    def right(self,event):
        self.shiftLR(1)
        self.dx = 1
        self.dy = 0
        self.collision()
        return True
    def up(self,event):
        self.shiftUD(-1)
        self.dx = 0
        self.dy = -1
        self.collision()
        return True
    def down(self,event):
        self.shiftUD(1)
        self.dx = 0
        self.dy = 1
        self.collision()
        return True


    def collision(self):
        if self.head.x == self.curBall.x and self.head.y == self.curBall.y:
            self.addBall()
            added = self.addNode()
            return added
        return False
    
    def addNode(self): #NEEDS WORK
        if not self.head:
            self.head = Node()
            self.head.x = 0
            self.head.y = 0
            self.size += 1
            return True
        #GET LAST NODE
        temp = self.head
        while(temp.next):
            temp = temp.next


        incrementX = 1
        startX = -1
        endX = 2
    
        incrementY = 1
        startY = -1
        endY = 2

        if self.dx:
            startX *= self.dx
            endX *= self.dx
            incrementX *= self.dx
        elif self.dy:
            startY *= self.dy
            endY *= self.dy
            incrementY *= self.dy
        
        for dx in range(startX,endX,incrementX):
            for dy in range(startY,endY,incrementY):
                if abs(dx) is not abs(dy):
                    x = temp.x + dx
                    y = temp.y + dy
                    if self.validIdx(x,y):
                        if not self.grid[y][x]:
                            add = Node()
                            add.x = x
                            add.y = y
                            temp.next = add
                            add.prev = temp

                            self.size+=1
                            return True
        return False
                        
            
    def validIdx(self,x,y):
        if x>=0 and x<self.length and y>=0 and y<self.length:
            return True
        return False
    
    def shiftLR(self,direction):
        if not self.validIdx(self.head.x+direction,self.head.y):
            return False
        if self.grid[self.head.y][self.head.x+direction]:
            return False
        if not self.head.next:
            self.grid[self.head.y][self.head.x] = 0

        self.shift()
        
        self.head.x += direction
        return True
    
    def shiftUD(self,direction):
        if not self.validIdx(self.head.x,self.head.y+direction):
            return False
        if self.grid[self.head.y+direction][self.head.x]:
            return False
        if not self.head.next:
            self.grid[self.head.y][self.head.x] = 0
        temp = self.head

        self.shift()
        
        self.head.y += direction
        return True

    def shift(self):
        temp = self.head

        temp = self.head
        while temp.next:
            temp = temp.next
        
        per = temp.prev
        while per:
            temp.x = temp.prev.x
            temp.y = temp.prev.y
            temp = temp.prev
            per = per.prev

        return True

    def updateGrid(self):
        self.grid = [[0 for x in range(0,self.length)] for y in range(0,self.length)]
        temp = self.head
        while temp:
            self.grid[temp.y][temp.x] = temp
            temp = temp.next
        return True
        
    def print(self):
        node = self.head
        #print("---")
        temp = 1
        while(node):
            node.l['text'] = " "+str(temp)+" "
            temp += 1
            
            node.l.place(x = node.x*30,y = node.y*30)
            #print(node.x,node.y)
            node = node.next

        return True

    def printGrid(self):
        for row in self.grid:
            for item in row:
                if item:
                    print(1,end=" ")
                else:
                    print(0,end=" ")
            print()
        print()
        return True

    def addBall(self):
        if self.curBall:
            self.curBall.l.place_forget()
        if self.size == self.length*self.length:
            return False
        openSpot = False
        while not openSpot:
            x = random.choice(range(0,self.length))
            y = random.choice(range(0,self.length))
            openSpot = not self.grid[y][x]

            if openSpot:
                ball = Node()
                ball.l['text'] = ' O '
                ball.l['bg'] = 'red'
                ball.x = x
                ball.y = y
                self.curBall = ball
                ball.l.place(x = ball.x*30,y = ball.y*30)
    
                return True
        


game = LinkedList()
game.print()
game.addBall()

c.bind("<Left>",game.left)
c.bind("<Right>",game.right)
c.bind("<Up>",game.up)
c.bind("<Down>",game.down)
c.focus_set()
c.pack(fill= BOTH,expand = 1)

time = 0
move = True
while move:
    time += 50
    if game.dx:
        move = game.shiftLR(game.dx)
    elif game.dy:
        move = game.shiftUD(game.dy)
    

    #UPDATE GAME
    game.collision()
    game.updateGrid()
    game.print()
    

    
    root.after(100)
    root.update()

print("GAME OVER")
print('---------')
print('score :', game.size)

