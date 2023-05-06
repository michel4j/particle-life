import particle
from tkinter import Tk, Frame, Canvas
import random

canvasSize = 800


def genRandomParticles(numParticles, color):
    particles = []

    for i in range(numParticles):
        posX = random.uniform(0, canvasSize)
        posY = random.uniform(0, canvasSize)
        particles.append(particle.Particle(posX, posY, color))

    return particles

def main():
    window=Tk()
    
    canvas = Canvas(width=canvasSize, height=canvasSize, background='black')
    canvas.pack()

    particles = []

    whiteParticles = genRandomParticles(25, "white")
    redParticles = genRandomParticles(25, "red")
    blueParticles = genRandomParticles(25, "blue")

    particles.extend(whiteParticles)
    particles.extend(redParticles)
    particles.extend(blueParticles) 

    for prtcl in particles:
        canvas.create_oval(prtcl.posX, prtcl.posY, prtcl.posX + prtcl.size, prtcl.posY + prtcl.size, fill=prtcl.color)

    
    window.title('Particle Life')
    window.mainloop()
    

if __name__ == '__main__':
    main()