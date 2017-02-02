# MCS 260 Project Five by Maria Folvarska

from random import randint
from time import sleep

class Balloon(object):
    """
    Object-oriented model of a balloon.
    """
    def __init__(self, x, y, rad, pace, step, decr=1):
        """
        Creates the balloon with center (x,y) and radius = rad.
        The pace is how fast the balloon moves(how long the delay is)--
        if pace is shorter, the balloon deflates faster. 
        The step is how large of a stepsize the balloon can take.
        decr is the decrement the balloon decreases by with each update.
        """
        self.position = (x,y)
        self.ball_size = randint(1,rad)
        self.pace_deflate = pace 
        self.step_size = step 
        self.size_decr = decr 
        
    def deflate(self):
        """
        This function determines the random stepsize of the balloon,
        and adjusts the coordinates of its center (x,y) accordingly.
        It prints the position and radius of the balloon.
        """
        (xps, yps) = self.position
        swirlStep =  self.step_size
        nxp = xps + randint(-swirlStep, swirlStep)  
        nyp = yps + randint(-swirlStep, swirlStep)
        self.position = (nxp, nyp) #new position of center
        print('ballon center is at ' + str(self.position))
        print('radius is : ' + str(self.ball_size))
        
    def run(self):
        """
        The balloon swirls and deflates until radius = 0.
        """
        while self.ball_size > 0:  
            self.deflate() #deflates balloon
            sleep(self.pace_deflate)  #adds delay
            self.ball_size = self.ball_size - self.size_decr
            #the radius decreases by one
        
def main():
    """
    This main function is used for testing the class.
    """
    a = Balloon(40, 50, 10, 2, 5)
    print(a.run())
    b = Balloon(40, 50, 10, 1, 5)
    print(b.run())
    

if __name__ == '__main__':
    main()
