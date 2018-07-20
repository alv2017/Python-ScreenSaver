from tkinter import Tk, Canvas, BOTH
from random import randint, random, uniform
from math import sin, cos, pi

def generate_random_color():
    """
        Function returns a randomly generated color (as hex string)
        Example: "#ffa500" (this is a hex value for orange)
    """
    clr = "#%06X" % randint(0, 256**3-1)
    return clr

# GCD function
def gcd(a, b):
    """
        Returns a greatest common divisor of two integers
        (int, int) -> int
    """
        
    while( a % b != 0 ):
        a, b = b, a % b
    return b


class Spirograph():
    """
        Sprirograph parameters and geometry
    """
    def __init__(self, xc, yc, rSmall, rBig, l):
        
        # spirograph parameters
        self.xc = xc
        self.yc = yc
        self.rSmall = rSmall
        self.rBig = rBig
        self.l = l
        
        # number of periods the curve needs to complete itself
        self.nRot = self.rSmall // gcd(self.rSmall, self.rBig)
        
        # number of revolutions we are going to do: in case we do not want a full spiro
        self.rv = min(30, self.nRot) 
        
        # coefficient k
        self.k = self.rSmall / self.rBig
                
    def getXcoord(self, alpha):
        """
            computes x-coordinate of spiro for angle alpha in radians
        """
        v1 = (1 - self.k) * cos(alpha)
        v2 = self.l * self.k * cos(alpha*(1/self.k -1))
        return self.xc + self.rBig * ( v1 + v2  )
        
    def getYcoord(self, alpha):
        """
            computes y-coordinate of spiro for angle alpha in radians
        """
        v1 = (1 - self.k) * sin(alpha)
        v2 = self.l * self.k * sin(alpha*(1/self.k -1))
        return self.yc + self.rBig * ( v1 - v2  )   
        
    def points(self):
        """
            Returns array of spirograph points based on given parameters
        """
        step = 5
        points = []
        
        T = self.rv
        
        for alpha in range(0, 360 * T + step, step):
            theta = alpha * pi / 180
            x = self.getXcoord(theta)
            y = self.getYcoord(theta)
            points.append( x )
            points.append( y )
            
        return points
    
class SpiroImage():
    """
        This class takes care of Spirograph image
        It takes a Spirograph class object and Tk.Canvas
        as input parameters.
    """
    def __init__(self, spiro, canvas):
        self.spiro = spiro # Spirograph class object
        self.canvas = canvas # Tkinter.Canvas object
        
        # spiro drawing parameters
        self.lwidth = uniform(0.75, 1.5) # spiro line width
        self.color = generate_random_color() # spiro color
        
        # spiro moving parameters
        self.velocityX = randint(5, 10) * (-1)**randint(0,1)
        self.velocityY = randint(5, 10) * (-1)**randint(0,1)
                
    def check_bounds(self):
        screen_width = self.canvas.winfo_screenwidth()
        screen_height = self.canvas.winfo_screenheight()
        R = self.spiro.rBig
        
        xc = self.spiro.xc
        yc = self.spiro.yc
        
        if not 10+R < xc < screen_width - R-10:
            self.velocityX = -self.velocityX
            self.color = generate_random_color()
            self.canvas.itemconfig(self.image, fill=self.color)
            self.lwidth = random()+1
            
        if not 10+R < yc < screen_height - R-10:
            self.velocityY = -self.velocityY
            self.color = generate_random_color()
            self.canvas.itemconfig(self.image, fill=self.color)
            self.lwidth = random()+1
                   
    def move(self):
        self.check_bounds()
        self.spiro.xc += self.velocityX
        self.spiro.yc += self.velocityY
        self.canvas.move(self.image, self.velocityX, self.velocityY)
        
    def draw(self):
        w = self.canvas
        points = self.spiro.points()
        self.image = w.create_line(points, width=self.lwidth, fill=self.color)
        
    def animate(self):
        self.move()
        self.canvas.after(100, self.animate)
    
class ScreenSaver():
    spiros = []
    spiro_images = []
    def __init__(self, number_of_spiros):
        # app window
        self.root = Tk()
        self.N = number_of_spiros
        self.root.attributes('-fullscreen', True)
        
        # create canvas
        self.canvas = Canvas(self.root, bg="#6969cc")
        self.canvas.pack(expand=1, fill=BOTH)
        
        # generate spiros
        self.generate_spiros()
        # draw generated spiros
        self.draw_spiros()
        
        for seq in ('<Any-KeyPress>', '<Any-Button>', '<Motion>'):
            self.root.bind(seq, self.quit_screensaver)
            
        self.root.mainloop()
        
    def generate_spiros(self):
        """
            Generates a list of spiros to be displayed by screensaver.
            Generated spiros are saved to list called spiros
        """
        screen_width = self.canvas.winfo_screenwidth()
        screen_height = self.canvas.winfo_screenheight()
        
        for i in range(self.N):
            # spiro parameters
            rBig = randint(75, 175)
            rSmall = randint(50, rBig - 10)
            l = random()
            xc = randint(screen_width//2 - 100, screen_width//2 + 100)
            yc = randint(screen_height//2 - 100, screen_height//2 + 100)
            
            s = Spirograph(xc, yc, rSmall, rBig, l)
            self.spiros.append(s)
        
    def draw_spiros(self):
        """
            Draws spiros from the spiros list, the images can be accessed
            using the spiro_images list
        """
        for spiro in self.spiros:
            spiro_image = SpiroImage(spiro, self.canvas)
            self.spiro_images.append(spiro_image)
            spiro_image.draw()
            spiro_image.animate()
                        
    def quit_screensaver(self, e):
        self.root.destroy()
            
if __name__=='__main__':
    # n - a number of spiros displayed
    n = randint(8, 15)
    # statr screensaver
    ScreenSaver(n)