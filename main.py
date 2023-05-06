import particle
from tkinter import Tk, Frame, Canvas
import random
import math
import time

canvasSize = 800
dt = 0.02
particles = []


def genRandomParticles(numParticles, color):
    particles = []

    for i in range(numParticles):
        posX = random.uniform(0, canvasSize)
        posY = random.uniform(0, canvasSize)
        particles.append(particle.Particle(posX, posY, color))

    return particles

def rule(particle1, particle2, g):
    
    fx = 0
    fy = 0
    
    a = particle1
    b = particle2

    dx = a.posX - b.posX
    dy = a.posY - b.posY
    d = math.sqrt(dx*dx + dy*dy)
    if (d > 0):
        F = -g * 1/d
        fx += (F * dx)
        fy += (F * dy)
    
    a.posX += fx
    a.posY += fy

def update():

    rule(particles[0], particles[1], 1)


    # move particles
    object = 1
    for prtcl in particles:
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

    particles.append(particle.Particle(400, 400, "blue"))
    particles.append(particle.Particle(600, 600, "red"))

    # redParticles = genRandomParticles(1, "red")
    # blueParticles = genRandomParticles(1, "blue")

    for prtcl in particles:
        canvas.create_oval(prtcl.posX, prtcl.posY, prtcl.posX + prtcl.size, prtcl.posY + prtcl.size, fill=prtcl.color)

    while True:
        update()
        window.update_idletasks()
        window.update()
        time.sleep(dt)
    
if __name__ == '__main__':
    main()