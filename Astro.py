class Astro:
    def __init__(self,canvas,weight,radius,locationX,locationY,canvasLocationX,canvasLocationY,velocityX,velocityY,color):
        self.canvas=canvas
        self.weight=weight
        self.radius=radius
        self.locationX=locationX
        self.locationY=locationY
        self.velocityX=velocityX
        self.velocityY=velocityY
        self.color=color
        self.id=canvas.create_oval(locationX-radius/2,locationY-radius/2,locationX+radius/2,locationY+radius/2,fill=color,width=0)
        self.canvas.move(self.id,canvasLocationX,canvasLocationY)
        self.isSelected=False
        self.isSelectedID=-1
    def draw(self):
        #print("hi"+str(self.locationX))
        self.locationX=self.locationX+self.velocityX
        self.locationY=self.locationY+self.velocityY
        self.canvas.move(self.id,self.velocityX,self.velocityY)
        if self.isSelected:
            self.canvas.move(self.isSelectedID,self.velocityX,self.velocityY)
        #self.canvas.create_oval(self.locationX-self.radius/2,self.locationY-self.radius/2,self.locationX+self.radius/2,self.locationY+self.radius/2,fill=self.color,width=0)
    def applyForce(self,subAstro):
        leng=(self.locationX-subAstro.locationX)**2+(self.locationY-subAstro.locationY)**2
        if leng**0.5>((self.radius+subAstro.radius)/2):
            force=0.005*self.weight*subAstro.weight/(leng*self.weight)
            forceX=force*((subAstro.locationX-self.locationX))/(leng**0.5)
            forceY=force*((subAstro.locationY-self.locationY))/(leng**0.5)
            self.velocityX=self.velocityX+forceX
            self.velocityY=self.velocityY+forceY
            
            cacheLocationX=self.locationX+self.velocityX
            cacheLocationY=self.locationY+self.velocityY
            cacheleng=(cacheLocationX-subAstro.locationX)**2+(cacheLocationY-subAstro.locationY)**2
            if cacheleng**0.5<((self.radius+subAstro.radius)/2):
                self.velocityX=(self.velocityX*(self.weight-subAstro.weight)+2*subAstro.weight*subAstro.velocityX)/(self.weight+subAstro.weight)
                self.velocityY=(self.velocityY*(self.weight-subAstro.weight)+2*subAstro.weight*subAstro.velocityY)/(self.weight+subAstro.weight)
        else:
            self.velocityX=(self.velocityX*(self.weight-subAstro.weight)+2*subAstro.weight*subAstro.velocityX)/(self.weight+subAstro.weight)
            self.velocityY=(self.velocityY*(self.weight-subAstro.weight)+2*subAstro.weight*subAstro.velocityY)/(self.weight+subAstro.weight)
        
        '''
        print("subAstroX"+str(subAstro.locationX))
        print("subAstroY"+str(subAstro.locationY))
        print("selfX"+str(self.locationX))
        print("selfY"+str(self.locationY))
        print("forceX"+str(forceX))
        print("forceY"+str(forceY))
        '''
        #print(forceX)
        #print(forceY)

    def select(self,canvasLocationX,canvasLocationY):
        self.isSelectedID=self.canvas.create_oval(self.locationX-self.radius/2-4,self.locationY-self.radius/2-4,self.locationX+self.radius/2+4,self.locationY+self.radius/2+4,width=2)
        self.canvas.move(self.isSelectedID,canvasLocationX,canvasLocationY)
        self.isSelected=True
    def disSelect(self):
        self.canvas.delete(self.isSelectedID)
        self.isSelected=False
        

        
