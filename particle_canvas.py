import random
import particle
import time

class ParticleCanvas():
    
    def __init__(self, 
                 particles_per_color = 50, 
                 colors = ['red', 'green', 'blue'], 
                 canvas_border = False, 
                 particle_size = 2, 
                 canvas_size = {'Width': 1200, 'Height': 1200}, 
                 debug = False):
        # Canvas
        self.canvas_border = canvas_border
        self.canvas_size = canvas_size

        # Particles
        self.particles_per_color = particles_per_color
        self.colors = colors
        self.particle_size = particle_size
        self.particles = self.generateRandomParticles()
        self.attractionMatrix = self.generateRandomAttractionMatrix()

        self.debug = debug

    def update(self):
        """ Update particle canvas """
        if(self.debug):
            begin = time.time_ns()  / (10 ** 9)

        self.updateParticlePositions()

        if(self.debug):
            print("2. Adjust particle coordinates on canvas: \t" + str(time.time_ns()  / (10 ** 9) - begin) + " seconds")
    
    def generateRandomParticles(self):      
        """ Generate random particles for each color.
            Returns list of generatd particles""" 
        particles = []

        for color in self.colors:
            for i in range(self.particles_per_color):
                posX = random.uniform(0, self.canvas_size['Width'])
                posY = random.uniform(0, self.canvas_size['Height'])
                particles.append(particle.Particle(posX, posY, color))

        return particles

    def generateRandomAttractionMatrix(self):
        """ Generate random attraction matrix. 
            Values are between -1 and 1"""
        matrix = [[0 for x in range(len(self.colors))] for y in range(len(self.colors))]
        for i in range(len(self.colors)):
            for j in range(len(self.colors)):
                matrix[i][j] = random.uniform(-1, 1)
        return matrix
    
    def updateParticlePositions(self):
        """ Update particle positions """
        for prtcl in self.particles:
            self.updateParticlePosition(prtcl)

    def updateParticlePosition(self, prtcl):
        """ Update particle position based on velocity """
        if(self.canvas_border):
            # revert velocity if particle is out of bounds
            prtcl.posX += prtcl.velX
            if prtcl.posX > self.canvas_size['Width'] or prtcl.posX < 0:
                prtcl.posX -= prtcl.velX

            prtcl.posY += prtcl.velY
            if prtcl.posY > self.canvas_size['Height'] or prtcl.posY < 0:
                prtcl.posY -= prtcl.velY
        else:
            # wrap particle around canvas if out of bounds
            prtcl.posX += prtcl.velX
            if prtcl.posX > self.canvas_size['Width']:
                prtcl.posX = 0
            
            if prtcl.posX < 0:
                prtcl.posX = self.canvas_size['Width']

            prtcl.posY += prtcl.velY
            if prtcl.posY > self.canvas_size['Height']:
                prtcl.posY = 0

            if prtcl.posY < 0:
                prtcl.posY = self.canvas_size['Height']

    def returnExampleAttractionMatrices(self, matrixNumber):
        """ Returns example attraction matrices """
        matrix = []
        match matrixNumber:
            case 1:
                matrix =[   [   1,   0.8,    0.6,   0.4], 
                            [ 0.8,   1,      0.8,   0.6],
                            [ 0.6,   0.8,      1,   0.8],
                            [ 0.4,   0.6,    0.8,   1  ]]
                
            case 2:
                matrix =[   [ 0.3,  -0.5,   -0.3,   0.3], 
                            [   1,   0.5,      1,   0.5],
                            [-0.5,     1,    0.5,    -1],
                            [-0.3,     1,    0.5,   0.8]]
                
            case 3:
                matrix =[   [  -1,   0.8,    0.6,   0.4], 
                            [ 0.8,    -1,    0.8,   0.6],
                            [ 0.6,   0.8,     -1,   0.8],
                            [ 0.4,   0.6,    0.8,    -1]]
                
            case 4:
                matrix =[   [  -1,   0.8,    0.6,   0.4], 
                            [ 0.8,    -1,   -0.8,   0.6],
                            [-0.6,   0.8,     -1,   0.8],
                            [ 0.4,  -0.6,    0.8,    -1]]
            
            case 5:
                matrix =[   [   1,   0.2,      0,  -0.2], 
                            [-0.2,     1,    0.2,     0],
                            [   0,  -0.2,      1,   0.2],
                            [ 0.2,     0,   -0.2,     1]]
                
            case 6:
                matrix =[   [   1,     1,      0,     0], 
                            [   1,    -1,     -1,     0],
                            [   0,    -1,     -1,     1],
                            [   0,     0,      1,     1]]
                
            case _:
                matrix = self.generateRandomAttractionMatrix()
        
        return matrix