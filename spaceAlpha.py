from tkinter import *
from os.path import expanduser
from Astro import *
from SpaceShip import *

import time

drawEvent=False
pauseEvent=True
lockEvent=False
backgroundColor='white'
astroColor='orange'
versionGet='spaceAlpha v?.?.?'
buildGet='??'
buildDateGet='????????'
canvasWidth=700
canvasHeight=700
changedX=0
changedY=0

def getVersion():
    global versionGet
    global buildGet
    global buildDateGet
    versionFile=open("version.txt",'r')
    versionGet = versionFile.readline().strip()
    buildGet = versionFile.readline().strip()
    buildDateGet = versionFile.readline().strip()

def move(event):
    global changedX
    global changedY
    if event.keysym=='Up':
        for i in astro:
            canvas.move(i.id,0,-10)
            if i.isSelected:
                canvas.move(i.isSelectedID,0,-10)
        changedY=changedY-10
    elif event.keysym=='Down':
        for i in astro:
            canvas.move(i.id,0,10)
            if i.isSelected:
                canvas.move(i.isSelectedID,0,10)
        changedY=changedY+10
    elif event.keysym=='Left':
        for i in astro:
            canvas.move(i.id,-10,0)
            if i.isSelected:
                canvas.move(i.isSelectedID,-10,0)
        changedX=changedX-10
    elif event.keysym=='Right':
        for i in astro:
            canvas.move(i.id,10,0)
            if i.isSelected:
                canvas.move(i.isSelectedID,10,0)
        changedX=changedX+10

def findSelectedAstro(astro):
    for i in astro:
        if i.isSelected:
            return [True, i]
    return [False, 0]

def clearSelectedAstro():
    global astro
    for i in astro:
        if i.isSelected:
            i.remove()
            del astro[astro.index(i)]

def clearAllAstro():
    global astro

    while len(astro)>0:
        astro[0].remove()
        del astro[0]
        
def addAstro(event):
    global changedX
    global changedY
    global astro
    global sizeEntry
    global weightEntry
    global eccentricityEntry
    global clockWiseEntry
    sunFindCache=findSelectedAstro(astro)
    astroWeight=float(weightEntry.get())
    astroSize=float(sizeEntry.get())
    locationX=event.x-changedX
    locationY=event.y-changedY
    if sunFindCache[0]:
        sun=sunFindCache[1]
        clockWise=str(clockWiseEntry.get())
        print(changedX)
        leng=((locationX-sun.locationX)**2+(locationY-sun.locationY)**2)**0.5
        velocity=(0.005*sun.weight/leng)**0.5
        velocityX=-velocity*((sun.locationY-locationY))/leng
        velocityY=velocity*((sun.locationX-locationX))/leng
        if clockWise=="yes":
            velocityX=-velocityX
            velocityY=-velocityY
        velocityX=velocityX+sun.velocityX
        velocityY=velocityY+sun.velocityY
        astro.append(Astro(canvas,astroWeight,astroSize,locationX,locationY,changedX,changedY,velocityX,velocityY,astroColor))
    else:
        astro.append(Astro(canvas,astroWeight,astroSize,locationX,locationY,changedX,changedY,0,0,astroColor))
        
    

def selectAstro(event):
    for i in astro:
        if i.isSelected:
            i.disSelect()
    
    for i in astro:
        if (i.locationX+changedX+i.radius/2+4)>event.x and (i.locationX+changedX-i.radius/2-4)<event.x and (i.locationY+changedY+i.radius/2+4)>event.y and (i.locationY+changedY-i.radius/2-4)<event.y:
            i.select(changedX,changedY)
            break


def LButtonEvent(event):
    
    global drawEvent
    print("x:"+str(event.x)+" y:"+str(event.y))
    
    if drawEvent:
        addAstro(event)
        drawEvent=False
        
    else:
        selectAstro(event)
        print("can't draw")
        

def addAstroMode():
    global drawEvent
    drawEvent=True

def pauseMode():
    global pauseEvent
    pauseEvent=not pauseEvent

getVersion()
#main UI setup
#tk
tk=Tk()
tk.title(versionGet+' (build '+buildGet+', '+buildDateGet+')')
canvas=Canvas(tk, width=canvasWidth, height=canvasHeight)
canvas.pack()
tk.update()

menuTk=Tk()
menuTk.title('Options')
menuTk.update()

#tk>menu
def NewFile():
    global tk
    print ("New File!")
    clearAllAstro()
    pauseEvent=True
    tk.title(versionGet+' (build '+buildGet+', '+buildDateGet+')')

def SaveAsFile():
    print ("Save File!")
    global canvas
    global tk
    global backgroundColor
    global astro
    global changedX
    global changedY

    dataFile = filedialog.asksaveasfile(mode='w',initialdir = "/sample",defaultextension=".ml")

    # asksaveasfile return `None` if dialog closed with "cancel".
    if dataFile is None:
        return

    '''
    #setup tk title
    fileName=dataFile.split("/")[-1]
    tk.title(versionGet+" - "+fileName)
    '''
    
    dataFile.write("spaceAlpha:1.1.0\ncanvasColor:"+backgroundColor+"\ncanvasLocationX:0\ncanvasLocationY:0")
    for i in astro:
        dataFile.write("\n"+str(i.weight)+":"+str(i.radius)+":"+str(i.locationX+changedX)+":"+str(i.locationY+changedY)+":"+str(i.velocityX)+":"+str(i.velocityY)+":"+str(i.color))
    dataFile.close()
    

def OpenFile():
    global canvas
    global tk
    global backgroundColor
    name = filedialog.askopenfilename(initialdir = "/sample",filetypes = (("mileu files","*.ml"),("all files","*.*")))
    dataFile=open(name,'r')
    
    #checkFileType
    fileFormatCheck = dataFile.readline()
    
    if not fileFormatCheck.strip()=="spaceAlpha:1.1.0":
        dataFile.close()
        print("ERROR(1)! Incorrect file format.")
        return

    canvasColor = dataFile.readline()
    canvasLocationX = dataFile.readline()
    canvasLocationY = dataFile.readline()
    
    if canvasColor==None or canvasLocationX==None or canvasLocationY==None:
        dataFile.close()
        print("ERROR(2)! Incorrect file format.")
        return

    #setup tk title
    fileName=name.split("/")[-1]
    tk.title(versionGet+' - '+fileName)
    #setup before open file
    clearAllAstro()
    pauseEvent=True
    backgroundColor=canvasColor.split(':')[1].strip()
    canvas.config(background=backgroundColor)
    
    #C.L.X. = canvsLocationX
    CLX=float(canvasLocationX.split(':')[1])
    CLY=float(canvasLocationY.split(':')[1])
    
    while True:
        dataFileLineCache = dataFile.readline()
        if not dataFileLineCache: break
        #D.F.L.C. = DataFileLineCache
        DFLC=dataFileLineCache.strip().split(':')
        astro.append(Astro(canvas,float(DFLC[0]),float(DFLC[1]),float(DFLC[2])+CLX,float(DFLC[3])+CLY,changedX,changedY,float(DFLC[4]),float(DFLC[5]),str(DFLC[6])))
        print(dataFileLineCache)
    dataFile.close()
    print (name)

#lock view to selected astro
def ifLock():
    global lockEvent
    lockEvent=not lockEvent

def selectViewLock():
    cacheAstro=None
    for i in astro:
        if i.isSelected:
            cacheAstro=i

    if not cacheAstro:
        return

    #if using cacheAstro, then the data changed during for
    vx=cacheAstro.velocityX
    vy=cacheAstro.velocityY
    lx=cacheAstro.locationX
    ly=cacheAstro.locationY
    
    changedX=0
    changedY=0
    
    for i in astro:
        #i.velocityX=i.velocityX-vx
        #i.velocityY=i.velocityY-vy
        i.locationX=i.locationX-lx+canvasWidth/2
        i.locationY=i.locationY-ly+canvasHeight/2
        i.redraw()

def About():
    print ("This is a simple example of a menu")

#setup color of background and astro
def setBackgroundColor_black():
    global backgroundColor
    global canvas
    backgroundColor='black'
    canvas.config(background=backgroundColor)

def setBackgroundColor_snow():
    global backgroundColor
    global canvas
    backgroundColor='snow'
    canvas.config(background=backgroundColor)

def setBackgroundColor_cyan():
    global backgroundColor
    global canvas
    backgroundColor='cyan'
    canvas.config(background=backgroundColor)

def setBackgroundColor_aquamarine():
    global backgroundColor
    global canvas
    backgroundColor='aquamarine'
    canvas.config(background=backgroundColor)

def setBackgroundColor_lime_green():
    global backgroundColor
    global canvas
    backgroundColor='lime green'
    canvas.config(background=backgroundColor)

def setBackgroundColor_yellow():
    global backgroundColor
    global canvas
    backgroundColor='yellow'
    canvas.config(background=backgroundColor)

def setBackgroundColor_orange():
    global backgroundColor
    global canvas
    backgroundColor='orange'
    canvas.config(background=backgroundColor)

def setBackgroundColor_red():
    global backgroundColor
    global canvas
    backgroundColor='red'
    canvas.config(background=backgroundColor)

def setBackgroundColor_deep_pink():
    global backgroundColor
    global canvas
    backgroundColor='deep pink'
    canvas.config(background=backgroundColor)

def setBackgroundColor_purple():
    global backgroundColor
    global canvas
    backgroundColor='purple'
    canvas.config(background=backgroundColor)

def setBackgroundColor_dodger_blue():
    global backgroundColor
    global canvas
    backgroundColor='dodger blue'
    canvas.config(background=backgroundColor)

def setBackgroundColor_green():
    global backgroundColor
    global canvas
    backgroundColor='green'
    canvas.config(background=backgroundColor)



def setAstroColor_black():
    global astroColor
    astroColor='black'

def setAstroColor_snow():
    global astroColor
    astroColor='snow'

def setAstroColor_cyan():
    global astroColor
    astroColor='cyan'

def setAstroColor_aquamarine():
    global astroColor
    astroColor='aquamarine'

def setAstroColor_lime_green():
    global astroColor
    astroColor='lime green'

def setAstroColor_yellow():
    global astroColor
    astroColor='yellow'

def setAstroColor_orange():
    global astroColor
    astroColor='orange'

def setAstroColor_red():
    global astroColor
    astroColor='red'

def setAstroColor_deep_pink():
    global astroColor
    astroColor='deep pink'

def setAstroColor_purple():
    global astroColor
    astroColor='purple'

def setAstroColor_dodger_blue():
    global astroColor
    astroColor='dodger blue'

def setAstroColor_green():
    global astroColor
    astroColor='green'


menu=Menu(tk)
tk.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=NewFile, accelerator="Command-N")
filemenu.add_command(label="Save As...", command=SaveAsFile, accelerator="Command-S")
filemenu.add_command(label="Open...", command=OpenFile, accelerator="Command-O")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=canvas.quit)

#lock view menu
viewMenu = Menu(menu)
menu.add_cascade(label="View", menu=viewMenu)
viewMenu.add_command(label="Lock View", command=ifLock)

#set color menu
colorMenu = Menu(menu)
menu.add_cascade(label="Color", menu=colorMenu)

backgroundColorMenu = Menu(menu)
colorMenu.add_cascade(label="Background", menu=backgroundColorMenu)
backgroundColorMenu.add_command(label="black", command=setBackgroundColor_black)
backgroundColorMenu.add_command(label="snow", command=setBackgroundColor_snow)
backgroundColorMenu.add_command(label="cyan", command=setBackgroundColor_cyan)
backgroundColorMenu.add_command(label="aquamarine", command=setBackgroundColor_aquamarine)
backgroundColorMenu.add_command(label="lime green", command=setBackgroundColor_lime_green)
backgroundColorMenu.add_command(label="yellow", command=setBackgroundColor_yellow)
backgroundColorMenu.add_command(label="orange", command=setBackgroundColor_orange)
backgroundColorMenu.add_command(label="red", command=setBackgroundColor_red)
backgroundColorMenu.add_command(label="deep pink", command=setBackgroundColor_deep_pink)
backgroundColorMenu.add_command(label="purple", command=setBackgroundColor_purple)
backgroundColorMenu.add_command(label="dodger blue", command=setBackgroundColor_dodger_blue)
backgroundColorMenu.add_command(label="green", command=setBackgroundColor_green)

astroColorMenu = Menu(menu)
colorMenu.add_cascade(label="Astro", menu=astroColorMenu)
astroColorMenu.add_command(label="black", command=setAstroColor_black)
astroColorMenu.add_command(label="snow", command=setAstroColor_snow)
astroColorMenu.add_command(label="cyan", command=setAstroColor_cyan)
astroColorMenu.add_command(label="aquamarine", command=setAstroColor_aquamarine)
astroColorMenu.add_command(label="lime green", command=setAstroColor_lime_green)
astroColorMenu.add_command(label="yellow", command=setAstroColor_yellow)
astroColorMenu.add_command(label="orange", command=setAstroColor_orange)
astroColorMenu.add_command(label="red", command=setAstroColor_red)
astroColorMenu.add_command(label="deep pink", command=setAstroColor_deep_pink)
astroColorMenu.add_command(label="purple", command=setAstroColor_purple)
astroColorMenu.add_command(label="dodger blue", command=setAstroColor_dodger_blue)
astroColorMenu.add_command(label="green", command=setAstroColor_green)

#help menu
helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)

#option panel

sizeLabel=Label(menuTk,text="size")
sizeLabel.grid(row=0, column=0)
sizeEntry=Entry(menuTk,width=10,justify=CENTER)
sizeEntry.insert(INSERT,"20")
sizeEntry.grid(row=0, column=1)

weightLabel=Label(menuTk,text="weight")
weightLabel.grid(row=1, column=0)
weightEntry=Entry(menuTk,width=10,justify=CENTER)
weightEntry.insert(INSERT,"100")
weightEntry.grid(row=1, column=1)

eccentricityLabel=Label(menuTk,text="eccentricity")
eccentricityLabel.grid(row=2, column=0)
eccentricityEntry=Entry(menuTk,width=10,justify=CENTER)
eccentricityEntry.insert(INSERT,"0")
eccentricityEntry.grid(row=2, column=1)

clockWiseLabel=Label(menuTk,text="clockWise")
clockWiseLabel.grid(row=3, column=0)
clockWiseEntry=Entry(menuTk,width=10,justify=CENTER)
clockWiseEntry.insert(INSERT,"yes")
clockWiseEntry.grid(row=3, column=1)

drawButton=Button(menuTk,text="draw",command=addAstroMode)
drawButton.grid(row=4, column=0)

resumeButton=Button(menuTk,text="pause/resume",command=pauseMode)
resumeButton.grid(row=4, column=1)

deleteButton=Button(menuTk,text="delete",command=clearSelectedAstro)
deleteButton.grid(row=5, column=0)

clearButton=Button(menuTk,text="clear all",command=clearAllAstro)
clearButton.grid(row=5, column=1)

astro=[]
num=1

#command key binding doesn't work well
canvas.bind_all("<Meta-N>", NewFile)
canvas.bind_all("<Meta-S>", SaveAsFile)
canvas.bind_all("<Meta-O>", OpenFile)
canvas.bind_all("<KeyPress-Up>",move)
canvas.bind_all("<KeyPress-Down>",move)
canvas.bind_all("<KeyPress-Left>",move)
canvas.bind_all("<KeyPress-Right>",move)
canvas.bind_all("<Button-1>",LButtonEvent)

#sample1 solar system
'''
for i in range(num):
    astro.append(Astro(canvas,62,10,300,200-17*i,changedX,changedY,2.7*(-1)**i,0,'green'))

astro.append(Astro(canvas,152000,30,300,300,changedX,changedY,0,0,'red'))
'''
#sample2 swingby
'''
astro.append(Astro(canvas,3052000,30,0,300,changedX,changedY,4,0,'red'))
astro.append(Astro(canvas,12,10,600,100,changedX,changedY,-2,0,'green'))
'''
#astro.append(Astro(canvas,15200000,30,300,300,changedX,changedY,0,0,'red'))

while 1:
    if not pauseEvent:
        for i in astro:
            for j in astro:
                if i!=j:
                    i.applyForce(j)
            i.draw()
            
    if lockEvent:
        selectViewLock()
    
    tk.update()
    #time.sleep(1/60)
