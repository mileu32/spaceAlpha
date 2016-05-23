from tkinter import *
from os.path import expanduser
from Astro import *
from SpaceShip import *

import time

drawEvent=False
pauseEvent=True
lockEvent=False
versionGet='spaceAlpha v?.?.?'
buildGet='??'
buildDataGet='????????'
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
        astro.append(Astro(canvas,astroWeight,astroSize,locationX,locationY,changedX,changedY,velocityX,velocityY,'orange'))
    else:
        astro.append(Astro(canvas,astroWeight,astroSize,locationX,locationY,changedX,changedY,0,0,'orange'))
        
    

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
    #issue button pause/resume
    if event.y>600 or event.y<20:
        return
    
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
    
    dataFile.write("spaceAlpha:0.3.0\ncanvasLocationX:0\ncanvasLocationY:0")
    for i in astro:
        dataFile.write("\n"+str(i.weight)+":"+str(i.radius)+":"+str(i.locationX+changedX)+":"+str(i.locationY+changedY)+":"+str(i.velocityX)+":"+str(i.velocityY)+":"+str(i.color))
    dataFile.close()
    

def OpenFile():
    global canvas
    global tk
    name = filedialog.askopenfilename(initialdir = "/sample",filetypes = (("mileu files","*.ml"),("all files","*.*")))
    dataFile=open(name,'r')
    
    #checkFileType
    fileFormatCheck = dataFile.readline()
    
    if not fileFormatCheck.strip()=="spaceAlpha:0.3.0":
        dataFile.close()
        print("ERROR(1)! Incorrect file format.")
        return
    canvasLocationX = dataFile.readline()
    canvasLocationY = dataFile.readline()
    
    if canvasLocationX==None or canvasLocationY==None:
        dataFile.close()
        print("ERROR(2)! Incorrect file format.")
        return

    #setup tk title
    fileName=name.split("/")[-1]
    tk.title(versionGet" - "+fileName)
    #setup before open file
    clearAllAstro()
    pauseEvent=True
    
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

menu=Menu(tk)
tk.config(menu=menu)
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=NewFile, accelerator="Command-N")
filemenu.add_command(label="Save As...", command=SaveAsFile, accelerator="Command-S")
filemenu.add_command(label="Open...", command=OpenFile, accelerator="Command-O")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=canvas.quit)

viewMenu = Menu(menu)
menu.add_cascade(label="View", menu=viewMenu)
viewMenu.add_command(label="Lock View", command=ifLock)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)

#under option
sizeLabel=Label(tk,text="size")
sizeLabel.pack(side="left")
sizeEntry=Entry(tk,width=3,justify=CENTER)
sizeEntry.insert(INSERT,"20")
sizeEntry.pack(side="left")

weightLabel=Label(tk,text="weight")
weightLabel.pack(side="left")
weightEntry=Entry(tk,width=3,justify=CENTER)
weightEntry.insert(INSERT,"100")
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
