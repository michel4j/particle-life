import random
import particle

class ParticleCanvas():
    
    def __init__(self, particlesPerColor = 50, colors = ['red', 'green', 'blue'], border = False, canvasSize = {'Width': 1200, 'Height': 1200}):
        # Canvas
        self.border = border
        self.canvasSize = canvasSize

        # Particles
        self.particlesPerColor = particlesPerColor
        self.colors = colors
        self.particles = self.generateRandomParticles()
        self.attractionMatrix = self.generateRandomAttractionMatrix()

    def generateRandomParticles(self):      
        """ Generate random particles for each color.
            Returns list of generatd particles""" 
        particles = []

        for color in self.colors:
            for i in range(self.particlesPerColor):
                posX = random.uniform(0, self.canvasSize['Width'])
                posY = random.uniform(0, self.canvasSize['Height'])
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
                matrix  [   [  -1,   0.8,    0.6,   0.4], 
                            [ 0.8,    -1,   -0.8,   0.6],
                            [-0.6,   0.8,     -1,   0.8],
                            [ 0.4,  -0.6,    0.8,    -1]]
                
            case _:
                matrix = self.generateRandomAttractionMatrix()
        
        return matrix