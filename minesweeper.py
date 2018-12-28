#Minesweeper
#Ravi Seth
#Mon June 1 2015

#PROGRAM HEADER
#PURPOSE : CREATE MINESWEEPER
#

from tkinter import*
import random
import time
myGui=Tk()

myGui.geometry("280x320+0+0")

myGui.title("Minesweeper")

canvas=Canvas(myGui)
canvas.pack(expand='yes',fill='both')




#l1=Label(canvas,text='damn!')
#myGui.after(1000,lambda:l1.pack())

def startTimer():
    global time
    time=time+1
    time_btn["text"]="Time : "+str(time)
    if finished==False:
        myGui.after(1000,startTimer)
    else:
        time_btn["text"]="Time : "+str(time-1)
        
class main():
    def DoSomething(x):
        global firstButtonPress
        firstButtonPress+=1
        if firstButtonPress==1:
            startTimer()
        #print (x)                 #This will print out “Button1” or “Button2” depending on which button is pressed
        name1=x.split("_")
        name1=name1[1]
        name1="place_"+name1
            
        flagText=eval(name1+"['text'] != '|>'")

        if flagText:
            y=x.split("_")
            if y[0]=="bomb":
                for bomb in bombs:
                    exec (bomb+".configure(text='x%*',font=('Impact',8),bg='red',fg='white')")
                complete=True
                checkForWin("lose")
                

                
            #IF NOT A BOMB, CHECK FOR NUMBER OF BOMBS AROUND
            else:
                #CHECK FOR NUMBER OF BOMBS
                number=0

                place=[int(i) for i in y[1]]

                xNum=int(place[1])
                yNum=int(place[0])

                zeros=[]
                for a in range (yNum-1,yNum+2):
                    for b in range (xNum-1,xNum+2):
                        if -1<a<board and -1<b<board:
                            coord=str(a)+str(b)
                            name2='place_'+str(coord)                            
                            #index1=(numbers.index(coord))

                            #name2=names[index1]

                            #bombOrNot=name1.split("_")
                            #bombOrNot=bombOrNot[0]

                            #print (coord,name1)
                            
                            #if bombOrNot=="bomb":
                            if name2 in bombs:
                                number=number+1

                            if coord!=y[1]:
                                zeros.append(coord)

                color=main.colour(number)
                exec (name1+".configure(text="+str(number)+",fg="+color+",bg='light grey')")
                #IF THE BOX CLICKED IS A ZERO
                zeros2=[]
                if number==0:
                    for zero in zeros:
                        zeros2=[]
                        number2=0
                        place=[int(i) for i in zero]
                        
                        xNum=int(place[1])
                        yNum=int(place[0])
                        for a in range (yNum-1,yNum+2):
                            for b in range (xNum-1,xNum+2):
                                if -1<a<board and -1<b<board:
                                    coord=str(a)+str(b)
                                    name2='place_'+str(coord)
                                    #index1=(numbers.index(coord))

                                    #name2=names[index1]

                                    #bombOrNot=name1.split("_")
                                    #bombOrNot=bombOrNot[0]


                                    #if zero=='23':
                                     #   print (coord,name1)

                                    #print (coord,name1)
                                    
                                    #if bombOrNot=="bomb":
                                    if name2 in bombs:
                                        number2=number2+1
                                    else:
                                        if coord not in zeros:
                                            zeros2.append(coord)

                        #indexNum=numbers.index(zero)
                        #name=names[indexNum]
                        name="place_"+str(zero)

                        flagText=eval(name+"['text'] != '|>'")
                        if flagText:
                            name1=name.split("_")
                            name1=name1[1]
                            name1="place_"+name1
                            if number2==0:
                                
                                for zeros2Go in zeros2:
                                    zeros.append(zeros2Go)
                                exec (name1+".configure(text='0',bg='light grey')")
                            else:
                                #print('num',name1)
                                #if name1=='place_01':
                                   # print (name1,number2)
                                exec (name1+".configure(text="+str(number2)+",bg='light grey')")
                            color=main.colour(number2)
                            exec (name1+".configure(fg="+color+")")

 
        checkForWin("win")


                        

            
    def colour(num):
        colours=["'light grey'","'blue'","'green'","'red'","'dark blue'","'brown'","'cyan'","'black'","'grey'"]
        color1=colours[num]
        return color1
                
    def flag(x):
        global score
        name1=x.split("_")
        name1=name1[1]
        name1="place_"+name1
        true=eval(name1+"['bg'] == 'light green'")
        question=eval(name1+"['text'] == '|>'")
        if true:
            if name1 not in flagged:
                flagged.append(name1)
                score=score-1
                exec(name1+".configure(text='|>')")
            elif question:
                score=score+1
                exec(name1+".configure(text='?')")
            else:
                flagged.remove(name1)

                exec(name1+".configure(text=' ')")
            bombs_btn["text"]="Bombs : "+str(score)
            checkForWin("win")

def checkForWin(x):
    global root
    global finished
    if x=='lose':
            finished=True
            root=Tk()
            root.title("Score")
            root.configure(bg='light green')
            #root.geometry("200x50+300+300")
            score_lbl=Label(root,text="LOST, hit bomb at "+str(time)+" sec").pack()
            play_btn=Button(root,text="Play Again",command=setup,width=10).pack()#(side='left',fill='x',expand='yes')
            done_btn=Button(root,text="Done",command=kill,width=10).pack()#(side='right',fill='x',expand='yes')
            leaderboard_btn=Button(root,text="Rank",command=leaderboard,width=10).pack()#(side='left',fill='x',expand='yes')
##            file1=open("practice.txt",'r')
##            file1Read=file1.readline()
##            file2=open("practice.txt",'w')
##            add=file1Read+"&?"+"Lost_"+str(time)
##            print (add)
##            file2.write(add)
    else:
        complete=False
        for a in names:
            colour=eval(a+"['bg']=='light grey'")
            text=eval(a+"['text']=='|>'")
            if colour or text:
                complete=True
            else:
                complete=False
                break
        if complete and score==0:
            finished=True
            root=Tk()
            root.title("Score")
            root.configure(bg='light green')
            #root.geometry("200x50+300+300")
            score_lbl=Label(root,text="Completed in "+str(time)+" sec").pack()
            play_btn=Button(root,text="Play Again",command=setup,width=10).pack()
            done_btn=Button(root,text="Done",command=kill,width=10).pack()
            leaderboard_btn=Button(root,text="Rank",command=leaderboard,width=10).pack()

            file1Read = ""
            try:
                file1=open("practice.txt",'r')
                file1Read=file1.readline()
                file1.close()
            except:
                pass
            file2=open("practice.txt",'w+')
            file2.write(file1Read+str(time)+"&")
        
def kill():
    root.destroy()
    myGui.destroy()

def leaderboard():
    file1Read = ""
    try:
        file1=open("practice.txt",'r')
        file1Read=file1.readline()
        file1.close()
    except:
        pass
            
    if (file1Read!=''):
        newLeads=[]
        leaders=file1Read.split("&")
        for a in range (0,len(leaders)):
            if leaders[a]!='':
                leaders[a]=int(leaders[a])
                newLeads.append(leaders[a])
        newLeads.sort()
        for a in newLeads:
            leaders_lbl=Label(root,text="Completed in "+str(a)+" sec").pack()
    else:
        leaders_lbl=Label(root,text="No Scores").pack()

    
#SETUP RESTART
#-------------------------------------------------------------------
def setup():
    global names,flagged,firstButtonPress,time,time_btn,board,total,xplace,yplace,numbers,ranBombs,score,bombs_btn,bombs,finished

    root.destroy()
    bombs_btn.forget()
    time_btn.forget()
    
    #RESETS THE BOARD
    for a in names:
        exec(a+"['bg']='light green'")
        exec(a+"['text']=' '")
    finished=False
    flagged=[]
    firstButtonPress=0
    time=0
    time_btn=Label(canvas,text="Time : "+str(0))
    time_btn.pack(side="bottom")
    board=9 
    total=0
    bombs=[]
    ranBombs=[]
    finished=False
    score=10
    bombs_btn=Label(canvas,text="Bombs : "+str(score))
    bombs_btn.pack(side="bottom")

    #CREATE THE CERTAIN BOMBS IN THE CERTAIN POSITIONS
    #CREATE THE RANDOM NUMBERS
    while len(ranBombs)<score:
        placeY=random.randrange(0,board)
        placeX=random.randrange(0,board)
        
        if int(str(placeY)+str(placeX)) not in ranBombs:
            ranBombs.append(int(str(placeY)+str(placeX)))
            
    for d in names:
        beginning=d.split("_")
        
        name1="place_"+beginning[1]
        if int(beginning[1]) in ranBombs:
            #make this a bomb
            name="bomb_"+beginning[1]
            exec(name1+".configure(command=lambda widget=name:main.DoSomething(widget),font=('Algerian',9),bg='light green',text=' ',fg='black')")
            bombs.append(name1)
        else:
            name="notBomb_"+beginning[1]
            exec(name1+".configure(command=lambda widget=name:main.DoSomething(widget),font=('Algerian',9),bg='light green',text=' ',fg='black')")
        
            

#-------------------------------------------------------------------
#-------------------------------------------------------------------

finished=False
flagged=[]
firstButtonPress=0
time=0
time_btn=Label(canvas,text="Time : "+str(time))
time_btn.pack(side="bottom")
board=9
total=0
xplace=10
yplace=10
numbers=[]
names=[]
bombs=[]
score=10
bombs_btn=Label(canvas,text="Bombs : "+str(score))
bombs_btn.pack(side="bottom")

ranBombs=[]
#CREATE THE RANDOM NUMBERS
while len(ranBombs)<score:
    placeY=random.randrange(0,board)
    placeX=random.randrange(0,board)
    if int(str(placeY)+str(placeX)) not in ranBombs:
        ranBombs.append(int(str(placeY)+str(placeX)))
#ranBombs=[00,12,17,25,30,33,53,60,67,82]
for b in range (0,board):
    for a in range (0,board):
        #ranNum=random.randrange(0,4)
        name1='place_'+str(b)+str(a)
        if int(str(b)+str(a)) in ranBombs:
            name="bomb_"+str(b)+str(a)
            exec(name1+"=Button(canvas,text=' ',bg='light green',command=lambda widget=name:main.DoSomething(widget))")
            exec(name1+".place(x="+str(xplace)+",y="+str(yplace)+")")
            total=total+1

            bombs.append(name1)
            #print (name)
        else:
            name="notBomb_"+str(b)+str(a)
            exec(name1+"=Button(canvas,text=' ',bg='light green',command=lambda widget=name:main.DoSomething(widget))")
            exec(name1+".place(x="+str(xplace)+",y="+str(yplace)+")")
            
        exec(name1+".bind('<Button-2>',lambda event, x=name:main.flag(x))")
            
        exec(name1+".configure(font=('Algerian',9))")
        names.append(name1)
        numbers.append(str(b)+str(a))
        xplace=xplace+30
    xplace=10
    yplace=yplace+30          



#-------------------------------------------------------------------
#main.setup()


















