# MCS 260 Project Five by Maria Folvarska

from tkinter import *
from class_thread import ThreadBalloon
from random import randint

class PopBalloons():
    """
    This is a game of popping balloons. 
    """
    def __init__(self, wdw,dim):
        """
        Creates a GUI for the game.
        """
        wdw.title('drawing swirling balloons')
        self.startdeflate = False #state of animation
        self.balloons = [] #list of objects of ThreadBalloon
        #creation of labels:
        self.msg = StringVar() #enables us to change the message
        self.msg.set('put mouse inside box to pop balloons')
        self.LBL = Label(wdw, textvariable=self.msg)
        self.LBL.grid(row=0, columnspan = 6)
        self.LBL1 = Label(wdw, text='count')
        self.LBL1.grid(row=0, column=7)
        self.LBL2 = Label(wdw, text='delay')
        self.LBL2.grid(row=0, column=8)
        self.LBL3 = Label(wdw, text='size')
        self.LBL3.grid(row=0, column=9)
        self.LBL4 = Label(wdw, text='step')
        self.LBL4.grid(row=0, column=10)
        #creation of canvas:
        self.dim = dim  #dimension
        self.CNV = Canvas(wdw,width=self.dim,height=self.dim,bg='white')
        self.CNV.grid(row=1,columnspan=6)
        #creation of buttons:
        self.BTT1 = Button(wdw, text='start',command=self.start)
        self.BTT1.grid(row=2, column=0, columnspan=2,sticky=E+W)
        self.BTT2 = Button(wdw, text='stop', command=self.stop)
        self.BTT2.grid(row=2, column=2, columnspan=2, sticky=E+W)
        self.BTT3 = Button(wdw, text='clear', command=self.clear)
        self.BTT3.grid(row=2, column=4, columnspan=2, sticky=E+W)
        #creation of score box:
        self.ENT=Entry(wdw)
        self.ENT.grid(row=2,column=7,columnspan=4)
        self.ENT.insert(INSERT, "score = 0") #set score to 0
        #creation of scales:
        self.count = DoubleVar()
        self.SC1= Scale(wdw, orient='vertical', from_=1, to=20, \
                        length=400,variable=self.count)
        self.SC1.set(10)
        self.SC1.grid(row=1,column=7)
        self.delay = DoubleVar()
        self.SC2= Scale(wdw, orient='vertical', from_=1, to=20, \
                        length=400,variable=self.delay)
        self.SC2.set(10)
        self.SC2.grid(row=1,column=8)
        self.size = DoubleVar()
        self.SC3= Scale(wdw, orient='vertical', from_=1, to=20, \
                        length=400,variable=self.size)
        self.SC3.set(10)
        self.SC3.grid(row=1,column=9)
        self.step = DoubleVar()
        self.SC4= Scale(wdw, orient='vertical', from_=1, to=20, \
                        length=400,variable=self.step)
        self.SC4.set(10)
        self.SC4.grid(row=1,column=10)
        #bind mouse events:
        self.CNV.bind("<Button-1>", self.button_pressed)
        self.CNV.bind("<ButtonRelease-1>", self.button_released)

    def new_balloon(self):
        """
        Defines a new balloon with center (x,y) randomly in the dimension
        of the canvas. The attributes for the balloon are obtained from
        the scales of the GUI. The balloon is appended to the list self.balloons.
        """
        x = randint(0,self.dim) 
        y = randint(0,self.dim)
        delay = int(self.delay.get())
        radius = int(self.size.get())
        step_size = int(self.step.get())
        name = chr(ord('a') + len(self.balloons)) #gives each thread a specific id
        balloon = ThreadBalloon(name, x , y, radius, delay, step_size) #creates thread
        self.balloons.append(balloon)    
            
    def draw_balloon(self):
        """
        This function realizes the balloons in the list
        self.balloons as circles on the GUI. If the radius
        of the balloon is 0, the balloon is deleted from the canvas
        and from the list.
        """
        dim = self.dim
        for balloon in self.balloons:
            (xps, yps) = balloon.position
            rad = balloon.ball_size #radius
            name = balloon.getName() #gets name of balloon
            self.CNV.delete(name) #deletes balloon
            #doughnut topology is applied to keep balloons on canvas as they swirl
            if xps < 0:
                xps = dim - xps
            if yps < 0:
                yps = dim - yps
            if xps > dim:
                xps = xps - dim
            if yps > dim:
                yps = yps - dim
            balloon.position = (xps, yps)
            if rad == 0:
                #makes balloon disappear
                self.CNV.delete(name)
                self.balloons.pop(self.balloons.index(balloon)) 
            else:
                #creates updated version of balloon
                self.CNV.create_oval(xps+rad, yps+rad, xps-rad, yps-rad, width =1, \
                                 outline = 'black', fill = 'red', tags=name)
    def start(self):
        """
        Starts all balloons and the animation.
        """
        try:
            assert(self.ENT.get() == 'score = 0') #checks if user has cleared
            assert(len(self.balloons)== 0) #doublechecks that no balloons on screen
            d = self.delay.get()
            c = self.count.get()  #gets the number of balloons the user wants
            self.startdeflate = True
            for n in range(int(c)): 
                self.new_balloon()    #creates new balloon
            for balloon in self.balloons:
                balloon.start()  #starts each thread in list
            while self.startdeflate:
                self.draw_balloon()   #draws balloons
                self.CNV.update() #updates canvas
                if len(self.balloons) == 0:
                    self.stop()     
        except:
           self.msg.set('you must press clear before beginning a new game!')
           #error msg if board not cleared
                
    def stop(self):
        """
        Stops the animation and sets step size to 0.
        """
        self.startdeflate = False
        self.msg.set('the game has stopped')
        for balloon in self.balloons:
            balloon.ball_size = 0
            
    def clear(self): 
        """
        Deletes all ballons from canvas and clears the score.
        """
        while len(self.balloons) > 0:
            self.balloons.pop(0)
        #resets the GUI to the original position
        self.CNV.delete(ALL)
        self.ENT.get()
        self.ENT.delete(0, END)
        self.ENT.insert(INSERT, 'score = 0')
        self.SC1.set(10)
        self.SC2.set(10)
        self.SC3.set(10)
        self.SC4.set(10)
        self.msg.set('put mouse inside box to pop balloons')
        
    def score_update(self, radius):
        """
        Gets the score from the entry widget and updates it by adding
        the radius of the balloon popped.
        """
        current = self.ENT.get()
        L = current.split('=')
        score = int(L[1])
        new_score = score + radius
        update = 'score = ' + str(new_score) 
        self.ENT.delete(0, END)
        self.ENT.insert(INSERT, update)

    def button_pressed(self, event):
        """
        Gives coordinates of a point pressed. 
        """
        self.msg.set("currently at [ " + str(event.x) + ", " + str(event.y) + \
                     " ]" + " release to pop balloon")

    def button_released(self, event):
        """
        Upon release of the mouse, if the distance from the mouse pointer
        (x1, y1) to the center of the nearest balloon (x2,y2) is less than
        or equal to the radius of the ballon, then the ballon is popped and
        the score is updated.
        """
        from math import sqrt
        for balloon in self.balloons:
            rad = balloon.ball_size #radius of balloon
            (x2, y2) = balloon.position 
            (x1, y1) = (event.x, event.y) 
            #apply distance formula
            xpart = (x2 - x1) ** 2 
            ypart = (y2 - y1) ** 2 
            dist = sqrt(xpart + ypart)
            if dist <= rad: #if distance if less than or equal to radius
                balloon.ball_size=0
                self.msg.set("popped balloon at [ " + str(x1) + \
                            ", " + str(y1) + " ]")
                self.score_update(rad)  #updates score using radius of balloon popped
                
def main():
    """
    Main function runs the game of popping balloons.
    """
    top = Tk()
    PopBalloons(top,400)
    top.mainloop()

if __name__ == '__main__':
    main()
    
