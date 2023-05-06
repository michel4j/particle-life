import math
import globals

class Engine():
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
        for prtcl in globals.particles:
            totalForceX = 0
            totalForceY = 0

            for otherPrtcl in globals.particles:
                if(otherPrtcl == prtcl):
                    continue
                # calculte distance between particles
                rx =  otherPrtcl.posX - prtcl.posX
                ry =  otherPrtcl.posY - prtcl.posY
                r = math.sqrt(rx**2 + ry**2)
                # check if distance is greater than 0 and less than rMax
                if ((r > 0) & (r < globals.rMax)):
                    f = Engine.force((r / globals.rMax), globals.matrix[otherPrtcl.color][prtcl.color])
                    totalForceX += f * rx / r
                    totalForceY += f * ry / r

            totalForceX *= globals.rMax
            totalForceY *= globals.rMax

            prtcl.velX *= globals.frictionFactor
            prtcl.velY *= globals.frictionFactor

            prtcl.velX += totalForceX * globals.dt
            prtcl.velY += totalForceY * globals.dt