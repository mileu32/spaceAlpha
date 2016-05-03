from tkinter import *
from os.path import expanduser
from Astro import *
from spaceShip import *

import time

drawEvent=False
pauseEvent=True
changedX=0
changedY=0

def move(event):
    global changedX
    global changedY
    if event.keysym=='Up':
        for i in astro:
            canvas.move(i.id,0,-10)
            if i.isSelected:
                canvas.move(i.isSelectedID,0,-10)
        canvas.move(sun.id,0,-10)
        if sun.isSelected:
            canvas.move(sun.isSelectedID,0,-10)
        changedY=changedY-10
    elif event.keysym=='Down':
        for i in astro:
            canvas.move(i.id,0,10)
            if i.isSelected:
                canvas.move(i.isSelectedID,0,10)
        canvas.move(sun.id,0,10)
        if sun.isSelected:
            canvas.move(sun.isSelectedID,0,10)
        changedY=changedY+10
    elif event.keysym=='Left':
        for i in astro:
            canvas.move(i.id,-10,0)
            if i.isSelected:
                canvas.move(i.isSelectedID,-10,0)
        canvas.move(sun.id,-10,0)
        if sun.isSelected:
            canvas.move(sun.isSelectedID,-10,0)
        changedX=changedX-10
    elif event.keysym=='Right':
        for i in astro:
            canvas.move(i.id,10,0)
            if i.isSelected:
                canvas.move(i.isSelectedID,10,0)
        canvas.move(sun.id,10,0)
        if sun.isSelected:
            canvas.move(sun.isSelectedID,10,0)
        changedX=changedX+10


def addAstro(event):
    global changedX
    global changedY
    global astro
    global sizeEntry
    global weightEntry
    global eccentricityEntry
    global clockWiseEntry
    global sun
    astroWeight=int(weightEntry.get())
    astroSize=int(sizeEntry.get())
    clockWise=str(clockWiseEntry.get())
    print(changedX)
    locationX=event.x-changedX
    locationY=event.y-changedY
    leng=((locationX-sun.locationX)**2+(locationY-sun.locationY)**2)**0.5
    velocity=(0.005*sun.weight/leng)**0.5
    velocityX=-velocity*((sun.locationY-locationY))/leng
    velocityY=velocity*((sun.locationX-locationX))/leng
    if clockWise=="yes":
        velocityX=-velocityX
        velocityY=-velocityY
    velocityX=velocityX+sun.velocityX
    velocityY=velocityY+sun.velocityY
    astro.append(Astro(canvas,astroWeight,astroSize,locationX,locationY,changedX,changedY,velocityX,velocityY,'orange'))
    

def selectAstro(event):
    '''
    for i in astro:
            if(i.locationX+changedX+<event.
    '''

def LButtonEvent(event):
    
    global drawEvent
    
    if drawEvent:
        print("x:"+str(event.x)+" y:"+str(event.y))
        addAstro(event)
        drawEvent=False
        
    else:
        print("can't draw")
        

def addAstroMode():
    global drawEvent
    drawEvent=True

def pauseMode():
    global pauseEvent
    pauseEvent=not pauseEvent

#main UI setup
#tk
tk=Tk()
tk.title("spaceAlpha v0.3.0b1 (build 12, 20160503)")
canvas=Canvas(tk, width=600, height=600)
canvas.pack()
tk.update()

#tk>menu
def NewFile():
    print ("New File!")
def OpenFile():
    name = filedialog.askopenfilename(initialdir = expanduser('~')+"/Documents/spaceAlpha",filetypes = (("mileu files","*.ml"),("all files","*.*")))
    print (name)
def About():
    print ("This is a simple example of a menu")

menu=Menu(tk)
tk.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=NewFile)
filemenu.add_command(label="Open...", command=OpenFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=canvas.quit)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)

#under option
sizeLabel=Label(tk,text="size")
sizeLabel.pack(side="left")
sizeEntry=Entry(tk,width=3,justify=CENTER)
sizeEntry.insert(INSERT,"10")
sizeEntry.pack(side="left")

weightLabel=Label(tk,text="weight")
weightLabel.pack(side="left")
weightEntry=Entry(tk,width=3,justify=CENTER)
weightEntry.insert(INSERT,"10")
weightEntry.pack(side="left")

eccentricityLabel=Label(tk,text="eccentricity")
eccentricityLabel.pack(side="left")
eccentricityEntry=Entry(tk,width=3,justify=CENTER)
eccentricityEntry.insert(INSERT,"0")
eccentricityEntry.pack(side="left")

clockWiseLabel=Label(tk,text="clockWise")
clockWiseLabel.pack(side="left")
clockWiseEntry=Entry(tk,width=3,justify=CENTER)
clockWiseEntry.insert(INSERT,"yes")
clockWiseEntry.pack(side="left")

drawButton=Button(tk,text="draw",command=addAstroMode)
drawButton.pack(side="left")

resumeButton=Button(tk,text="pause/resume",command=pauseMode)
resumeButton.pack(side="right")

astro=[]
num=1

canvas.bind_all("<KeyPress-Up>",move)
canvas.bind_all("<KeyPress-Down>",move)
canvas.bind_all("<KeyPress-Left>",move)
canvas.bind_all("<KeyPress-Right>",move)
canvas.bind_all("<Button-1>",LButtonEvent)

'''
for i in range(num):
    astro.append(Astro(canvas,62,10,300,200-17*i,changedX,changedY,2.7*(-1)**i,0,'green'))
'''
astro.append(Astro(canvas,12,10,600,100,changedX,changedY,-2,0,'green'))
sun = Astro(canvas,3052000,30,0,300,changedX,changedY,4,0,'red')
sun.select(changedX,changedY)
while 1:
    if not pauseEvent:
        
        for i in astro:
            for j in astro:
                if i!=j:
                    i.applyForce(j)
            i.applyForce(sun)
            i.draw()
    
        for i in astro:
            sun.applyForce(i)
        sun.draw()
    tk.update()
    #time.sleep(1/60)
