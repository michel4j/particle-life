import particle
from tkinter import Tk, Frame, Canvas
import random
import math
import time
import enum

class Color(enum.Enum):
   red = 1
   blue = 2
   green = 3

matrix =[[0,    1,     2,      3    ], 
         [1,    0.5,   -0.5,   -0.3 ], 
         [2,    1,     0.5,    1    ],
         [3,    -0.5,  1,      0.5  ]]

canvasSize = 800
dt = 0.02
rMax = 250
particles = []
frictionHalfLife = 0.04
frictionFactor = math.pow(0.5, dt / frictionHalfLife)


def genRandomParticles(numParticles, color):
    colorValue = getattr(Color, color).value
    
    particles = []

    for i in range(numParticles):
        posX = random.uniform(0, canvasSize)
        posY = random.uniform(0, canvasSize)
        particles.append(particle.Particle(posX, posY, colorValue))

    return particles

# a is attraction matrix value: make matrix or set hardcoded for now (what value?)
def force(r, a):
    beta = 0.3
    if (r < beta):
        return r / beta - 1
    elif((beta < r) & (r < 1)):
        return a * ( 1 - abs(2 * r - 1 - beta) / (1 - beta))
    else:
        return 0
        



def updateVelocities():
    for prtcl in particles:
        totalForceX = 0
        totalForceY = 0

        for otherPrtcl in particles:
            if(otherPrtcl == prtcl):
                continue
            # calculte distance between particles
            rx =  otherPrtcl.posX - prtcl.posX
            ry =  otherPrtcl.posY - prtcl.posY
            r = math.sqrt(rx**2 + ry**2)
            # check if distance is greater than 0 and less than rMax
            if ((r > 0) & (r < rMax)):
                f = force((r / rMax), matrix[otherPrtcl.color][prtcl.color])
                totalForceX += f * rx / r
                totalForceY += f * ry / r

        totalForceX *= rMax
        totalForceY *= rMax

        prtcl.velX *= frictionFactor
        prtcl.velY *= frictionFactor

        prtcl.velX += totalForceX * dt
        prtcl.velY += totalForceY * dt


def update():

    updateVelocities()


    # move particles
    object = 1
    for prtcl in particles:
        prtcl.posX += prtcl.velX
        prtcl.posY += prtcl.velY
        canvas.moveto(object, prtcl.posX, prtcl.posY)
        object += 1
    
    

def main():
    global window
    window=Tk()
    window.title('Particle Life')
    global canvas
    canvas = Canvas(width=canvasSize, height=canvasSize, background='black')
    canvas.pack()

    # whiteParticles = genRandomParticles(25, "white")
    # redParticles = genRandomParticles(25, "red")
    # blueParticles = genRandomParticles(25, "blue")

    # particles.extend(whiteParticles)
    # particles.extend(redParticles)
    # particles.extend(blueParticles) 

    redParticles = genRandomParticles(25, "red")
    blueParticles = genRandomParticles(25, "blue")

    particles.extend(redParticles)
    particles.extend(blueParticles)

    for prtcl in particles:
        stringValue = Color(prtcl.color).name
        canvas.create_oval(prtcl.posX, prtcl.posY, prtcl.posX + prtcl.size, prtcl.posY + prtcl.size, fill=stringValue)

    while True:
        update()
        window.update_idletasks()
        window.update()
        time.sleep(dt)
    
if __name__ == '__main__':
    main()