import particle
from tkinter import Tk, Frame, Canvas
import random

canvasSize = 800
dt = 0.02
particlesToDraw = []
particles = []


def genRandomParticles(numParticles, color):
    particles = []

    for i in range(numParticles):
        posX = random.uniform(0, canvasSize)
        posY = random.uniform(0, canvasSize)
        particles.append(particle.Particle(posX, posY, color))

    return particles

def update():




    # move particles
    object = 1
    for prtcl in particlesToDraw:
        # change to new value
        prtcl.posX += 1
        prtcl.posY += 1
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

    particlesToDraw.append(particle.Particle(400, 400, "blue"))
    particlesToDraw.append(particle.Particle(600, 600, "red"))

    for prtcl in particlesToDraw:
        particles.append(canvas.create_oval(prtcl.posX, prtcl.posY, prtcl.posX + prtcl.size, prtcl.posY + prtcl.size, fill=prtcl.color))

    while True:
        update()
        window.update_idletasks()
        window.update()
    
if __name__ == '__main__':
    main()