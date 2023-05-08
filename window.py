from tkinter import Tk, Frame, Canvas
import random
import particle
import globals

class Window():

    window=Tk()
    window.title('Particle Life')
    
    def __init__(self):
        global canvas
        canvas = Canvas(width=globals.canvasSizeXMax, height=globals.canvasSizeYMax, background='black')
        canvas.pack()

    def genRandomParticles(numParticles, color):
        colorValue = getattr(globals.Color, color).value
        
        particles = []

        for i in range(numParticles):
            posX = random.uniform(globals.canvasSizeXMin, globals.canvasSizeXMax)
            posY = random.uniform(globals.canvasSizeYMin, globals.canvasSizeYMax)
            particles.append(particle.Particle(posX, posY, colorValue))

        return particles

    def updateParticlePositions():
        object = 1
        for prtcl in globals.particles:
            
            if(globals.border):
                # revert velocity if particle is out of bounds
                prtcl.posX += prtcl.velX
                if prtcl.posX > globals.canvasSizeXMax or prtcl.posX < globals.canvasSizeXMin:
                    prtcl.posX -= prtcl.velX

                prtcl.posY += prtcl.velY
                if prtcl.posY > globals.canvasSizeYMax or prtcl.posY < globals.canvasSizeYMin:
                    prtcl.posY -= prtcl.velY
            else:
                # wrap particle around canvas if out of bounds
                prtcl.posX += prtcl.velX
                if prtcl.posX > globals.canvasSizeXMax:
                    prtcl.posX = globals.canvasSizeXMin
                
                if prtcl.posX < globals.canvasSizeXMin:
                    prtcl.posX = globals.canvasSizeXMax

                prtcl.posY += prtcl.velY
                if prtcl.posY > globals.canvasSizeYMax:
                    prtcl.posY = globals.canvasSizeYMin

                if prtcl.posY < globals.canvasSizeYMin:
                    prtcl.posY = globals.canvasSizeYMax

            canvas.moveto(object, prtcl.posX, prtcl.posY)
            object += 1
        
    def DrawParticles():
        for i in range(len(globals.Color)):
            globals.particles.extend(Window.genRandomParticles(150, globals.Color(i).name))

        for prtcl in globals.particles:
            stringValue = globals.Color(prtcl.color).name
            canvas.create_oval(prtcl.posX, prtcl.posY, prtcl.posX + prtcl.size, prtcl.posY + prtcl.size, fill=stringValue)
