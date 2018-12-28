from tkinter import*
myGui = Tk()
myGui.geometry('300x300+300+300')
myGui.configure(bg='black')

canvas_1 = Canvas(myGui,height=300,width=300,bg='white')

def draw_enemy():
    global enemies
    enemies=[]
    c=[5,5,35,35]
    inc=50
    for x in range (0,8):
        for y in range (0,2):
            
            enemy = canvas_1.create_rectangle(c[0] + inc * x, c[1] + inc * y,c[2] + inc * x,c[3] + inc * y,fill='blue',tag='key')#it goes x1,y1,x2,y2   x1=x placement y1=y placement x2=x width of rectangle y2=y height of rectangle
            
            
            enemies.append(enemy)

canvas_1.place(x=0,y=0)

killer = canvas_1.create_oval(190,280,230,320,outline='red',fill='purple',tag='killer')
canvas_1.update()

def enemy(name):    
    global canvas_1
    global a
    a=canvas_1.coords(name)
    myGui.after(1000,doThis,name)
    
def doThis(name):
    global canvas_1
    canvas_1.move(name,0,10)
    enemy(name)

def shot(name):
    global canvas_1
    global b
    b=canvas_1.coords(name)
    myGui.after(1,doThisAgain,name)
    
def doThisAgain(name):
    global canvas_1
    global loaded_gun
    canvas_1.move(name,0,-5)
    
    if loaded_gun==0:
        for x in enemies:
            a=canvas_1.coords(x)
            if a[0] <= b[0] <= a[0] + 30: 
                if b[1] <= a[1] + 30:
                    canvas_1.delete(x)            
                    enemies.remove(x) 
                    canvas_1.delete(name)
                    loaded_gun=1
                    break
           
    if b[1] < 0:
        
        canvas_1.delete(name) 
        loaded_gun = 1
        
##    if loaded_gun == 0: # furas
##        myGui.after(50, doThisAgain, "shot")
    if loaded_gun==0:       
        shot('shot')

def shooting():
    global loaded_gun
    c = canvas_1.coords("killer")
    bullet = canvas_1.create_rectangle(c[0]+18,c[1]-10,c[0]+23,c[1],fill='orange',tag='shot')
    loaded_gun=0
    shot('shot')
    

def on_key_press(event):
    global canvas #,loaded_gun
    
    c = canvas_1.coords("killer")

    if event.keysym == 'Left' and c[0] > 0:
        canvas_1.move("killer", -10,0)
    elif event.keysym == 'Right' and c[2] < 300:
        canvas_1.move("killer", 10, 0)
    elif event.keysym == 'space':
        if loaded_gun == 1:
            shooting()
##    elif event.keysym == 'Shift_L':
##        loaded_gun = 1
##        canvas.delete("shot")
    
myGui.bind_all('<Key>', on_key_press)
loaded_gun=1

draw_enemy()
enemy('key')




