import particle
from tkinter import Tk, Frame, Canvas
import random
import math
import time
import enum

class Color(enum.Enum):
   red = 0
   blue = 1
   green = 2

def generateRandomAccelerationMatrix():
    matrix = [[0 for x in range(len(Color)+1)] for y in range(len(Color)+1)]
    for i in range(len(Color)+1):
        for j in range(len(Color)+1):
            matrix[i][j] = random.uniform(-1, 1)
    return matrix

matrix = generateRandomAccelerationMatrix()

canvasSizeXMin = 0
canvasSizeXMax = 1000
canvasSizeYMin = 0
canvasSizeYMax = 1000

dt = 0.01
rMax = 120
particles = []
frictionHalfLife = 0.04
frictionFactor = math.pow(0.5, dt / frictionHalfLife)
border = False


def genRandomParticles(numParticles, color):
    colorValue = getattr(Color, color).value
    
    particles = []

    for i in range(numParticles):
        posX = random.uniform(canvasSizeXMin, canvasSizeXMax)
        posY = random.uniform(canvasSizeYMin, canvasSizeYMax)
        particles.append(particle.Particle(posX, posY, colorValue))

    return particles

# fuck me im not writing this function myself 
def force(r, a):
    beta = 0.3
    if (r < beta):
        return r / beta - 1
    elif((beta < r) & (r < 1)):
        return a * ( 1 - abs(2 * r - 1 - beta) / (1 - beta))
    else:
        return 0

def updateParticleVelocities():
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

def updateParticlePositions():
    object = 1
    for prtcl in particles:
        
        if(border):
            # revert velocity if particle is out of bounds
            prtcl.posX += prtcl.velX
            if prtcl.posX > canvasSizeXMax or prtcl.posX < canvasSizeXMin:
                prtcl.posX -= prtcl.velX

            prtcl.posY += prtcl.velY
            if prtcl.posY > canvasSizeYMax or prtcl.posY < canvasSizeYMin:
                prtcl.posY -= prtcl.velY
        else:
            # wrap particle around canvas if out of bounds
            prtcl.posX += prtcl.velX
            if prtcl.posX > canvasSizeXMax:
                prtcl.posX = canvasSizeXMin
            
            if prtcl.posX < canvasSizeXMin:
                prtcl.posX = canvasSizeXMax

            prtcl.posY += prtcl.velY
            if prtcl.posY > canvasSizeYMax:
                prtcl.posY = canvasSizeYMin

            if prtcl.posY < canvasSizeYMin:
                prtcl.posY = canvasSizeYMax

        canvas.moveto(object, prtcl.posX, prtcl.posY)
        object += 1

def update():

    updateParticleVelocities()
    updateParticlePositions()

def main():
    global window
    window=Tk()
    window.title('Particle Life')
    global canvas
    canvas = Canvas(width=canvasSizeXMax, height=canvasSizeYMax, background='black')
    canvas.pack()

    for i in range(len(Color)):
        particles.extend(genRandomParticles(50, Color(i).name))

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