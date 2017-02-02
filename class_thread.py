# MCS 260 Project Five by Maria Folvarska

from balloon import Balloon
from threading import Thread
from time import sleep

class ThreadBalloon(Thread, Balloon):
    """
    Exports balloons as threads.
    """
    def __init__(self, n, x, y, r, pace, step, decr=1):
        Thread.__init__(self, name=n)    #creates thread
        Balloon.__init__(self, x, y, r, pace, step, decr)
        
    def run(self):
        """
        The balloon moves until radius = 0.
        """
        while self.ball_size > 0:
            self.deflate() #balloon deflates
            sleep(self.pace_deflate)  #delay
            self.ball_size = self.ball_size - self.size_decr
            #the radius decreases by one

def main():
    """
    Runs a simple test on deflating balloons.
    """
    print('creating balloons')
    a = ThreadBalloon('a',0,0,2,1,3)
    b = ThreadBalloon('b',100,100, 4, 2, 2)
    a.start()
    b.start()
    a.join()
    b.join()

if __name__== "__main__":
    main()
    
