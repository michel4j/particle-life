import math
import time

class Engine():
    def __init__(self, particle_canvas, debug = False):
        # Time
        self.dt = 0.02

        # Particles 
        self.rMax = 180
        self.frictionHalfLife = 0.04
        self.frictionFactor = math.pow(0.5, self.dt / self.frictionHalfLife)
        self.forceFactor = 0.5
        
        # Canvas
        self.particleCanvas = particle_canvas

        self.debug = debug

    def update(self):
        """ Update particle velocities """
        if(self.debug):
            begin = time.time_ns()  / (10 ** 9)
        
        self.updateParticleVelocities()

        if(self.debug):
            print("1. Calculate forces between particles:\t\t" + str(time.time_ns()  / (10 ** 9) - begin) + " seconds")

    
    # fuck me im not writing this function myself 
    def force(self, r, a):
        beta = 0.3
        if (r < beta):
            return r / beta - 1
        elif((beta < r) & (r < 1)):
            return a * ( 1 - abs(2 * r - 1 - beta) / (1 - beta))
        else:
            return 0

    def updateParticleVelocities(self):
        for prtcl in self.particleCanvas.particles:
            totalForceX = 0
            totalForceY = 0

            for otherPrtcl in self.particleCanvas.particles:
                if(otherPrtcl == prtcl):
                    continue
                # calculte distance between particles
                rx =  otherPrtcl.posX - prtcl.posX
                ry =  otherPrtcl.posY - prtcl.posY

                # adjust for screen wrapping
                if abs(rx) > self.particleCanvas.canvas_size['Width'] / 2:
                    rx = self.particleCanvas.canvas_size['Width'] - abs(rx)
                if abs(ry) > self.particleCanvas.canvas_size['Height'] / 2:
                    ry = self.particleCanvas.canvas_size['Height'] - abs(ry)
                r = math.sqrt(rx**2 + ry**2)
                # check if distance is greater than 0 and less than rMax
                if ((r > 0) & (r < self.rMax)):
                    f = self.force((r / self.rMax), 
                                   self.particleCanvas.attractionMatrix
                                        [self.particleCanvas.colors.index(otherPrtcl.color)]
                                        [self.particleCanvas.colors.index(prtcl.color)])
                    totalForceX += f * rx / r
                    totalForceY += f * ry / r

            totalForceX *= self.rMax * self.forceFactor
            totalForceY *= self.rMax * self.forceFactor

            prtcl.velX *= self.frictionFactor
            prtcl.velY *= self.frictionFactor

            prtcl.velX += totalForceX * self.dt
            prtcl.velY += totalForceY * self.dt