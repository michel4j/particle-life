import random
import particle
import time
import engine

class ParticleCanvas():
    
    def __init__(self, 
                 total_particles = 50, 
                 particle_colors = ['red', 'green', 'blue'], 
                 canvas_border = False, 
                 particle_size = 2, 
                 canvas_size = {'Width': 1200, 'Height': 1200}, 
                 debug = False):
        # Canvas
        self.canvas_border = canvas_border
        self.canvas_size = {'Width': canvas_size['Width'], 'Height': canvas_size['Height']}
        self.UI_space = 200

        # Particles
        self.particles_per_color = round(total_particles / len(particle_colors))
        self.particle_colors = particle_colors
        self.particle_size = particle_size
        self.particles = self.generateRandomParticles()
        self.attractionMatrix = self.returnExampleAttractionMatrices(2)

        # Engine
        self.engine = engine.Engine(particle_canvas = self, debug = debug)

        self.debug = debug

    def update(self):
        """ Update particle canvas """
        self.engine.update()
    
    def generateRandomParticles(self):      
        """ Generate random particles for each color.
            Returns list of generatd particles""" 
        particles = []

        for color in self.particle_colors:
            for i in range(self.particles_per_color):
                posX = random.uniform(self.UI_space, self.canvas_size['Width'] + self.UI_space)
                posY = random.uniform(0, self.canvas_size['Height'])
                particles.append(particle.Particle(posX, posY, color))

        return particles

    def generateRandomAttractionMatrix(self):
        """ Generate random attraction matrix. 
            Values are between -1 and 1"""
        matrix = [[0 for x in range(len(self.particle_colors))] for y in range(len(self.particle_colors))]
        for i in range(len(self.particle_colors)):
            for j in range(len(self.particle_colors)):
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