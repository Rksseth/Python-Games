from tkinter import*

root = Tk()
root.title("Ping Pong")
canvas = Canvas(root)



class paddle(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 40
        self.r = canvas.create_rectangle(self.x,self.y,self.x+self.width,self.y+self.height,fill = "black")

class ball(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.diameter = 20
        self.speedX = 4
        self.speedY = 4
        self.c = canvas.create_oval(self.x,self.y,self.x+self.diameter,self.y+self.diameter,fill="red")

class game(object):
    def __init__(self):
        self.w = int(canvas['width'])
        self.h = int(canvas['height'])
        self.r = paddle(3,0)
        self.c = paddle(self.w-self.r.width,0)
        self.b = ball(150,150)
        self.shift = 5

    def down(self,event):
        self.shiftDown()
        return True
    def up(self,event):
        self.shiftUp()
        return True

    def validIdx(self,y):
        if y>=0 and y+self.r.height<=self.h:
            return True
        return False
    
    def shiftDown(self):
        if self.validIdx(self.r.y+self.shift):
            self.r.y = self.r.y+self.shift
            canvas.coords(self.r.r,self.r.x,self.r.y,self.r.x+self.r.width,self.r.y+self.r.height)
            canvas.update()
            return True
        return False

    def shiftUp(self):
        if self.validIdx(self.r.y-self.shift):
            self.r.y = self.r.y-self.shift
            canvas.coords(self.r.r,self.r.x,self.r.y,self.r.x+self.r.width,self.r.y+self.r.height)
            canvas.update()
            return True
        return False

    def checkWall(self):
        if self.b.x<0 or self.b.x+self.b.diameter>self.w:
            return False
        if self.b.y<0 or self.b.y+self.b.diameter> self.h:
            self.b.speedY *= -1
        return True

    def move(self):
        noWall = self.checkWall()
        if not noWall:
            return False
        self.b.x += self.b.speedX
        self.b.y += self.b.speedY
        canvas.coords(self.b.c,self.b.x,self.b.y,self.b.x+self.b.diameter,self.b.y+self.b.diameter)
        canvas.update()
        return True

    def collision(self):
        #CHECK IF BALL IS IN HUMAN PADDLE
        if self.r.x+self.r.width >= self.b.x and (self.b.y+self.b.y+self.b.diameter)/2 in range(self.r.y,self.r.y+self.r.height):
            self.b.speedX *= -1
            self.move()
        #CHECK IF BALL IS IN COMPUTER PADDLE
        if self.c.x <= self.b.x+self.b.diameter and (self.b.y+self.b.y+self.b.diameter)/2 in range(self.c.y,self.c.y+self.c.height):
            self.b.speedX *= -1
            self.move()
        return True

    def computer(self):
        if self.b.y == self.c.y:
            return False
        elif self.b.y < self.c.y:
            self.shiftUpComputer()
        else:
            self.shiftDownComputer()
        return True

    def shiftDownComputer(self):
        if self.validIdx(self.c.y+self.shift):
            self.c.y = self.c.y+self.shift
            canvas.coords(self.c.r,self.c.x,self.c.y,self.c.x+self.c.width,self.c.y+self.c.height)
            canvas.update()
            return True
        return False
    def shiftUpComputer(self):
        if self.validIdx(self.c.y-self.shift):
            self.c.y = self.c.y-self.shift
            canvas.coords(self.c.r,self.c.x,self.c.y,self.c.x+self.c.width,self.c.y+self.c.height)
            canvas.update()
            return True
        return False
        
        
        

g= game()
canvas.bind("<Down>",g.down)
canvas.bind("<Up>",g.up)
canvas.focus_set()
canvas.pack()

g.collision()

time = 0
noWall = True
while noWall:
    noWall = g.move()
    
    g.collision()
    g.computer()
    root.after(50)
    time += 50

print("SUCCESSFUL GAME")
root.mainloop()

