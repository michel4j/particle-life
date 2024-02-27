import random

import engine
import particle


class ParticleCanvas:

    def __init__(
            self, total_particles, particle_colors, number_of_colors, canvas_border, particle_size, canvas_size,
            current_demo_matrix, debug
    ):
        # Create instance of engine class
        self.engine = engine.Engine(particle_canvas=self, debug=debug)

        # Canvas
        self.canvas_border = canvas_border
        self.canvas_size = {'Width': canvas_size['Width'], 'Height': canvas_size['Height']}
        self.UI_space = 200

        # Particles
        self.total_particles = total_particles
        self.number_of_colors = number_of_colors
        self.particles_per_color = round(self.total_particles / self.number_of_colors)
        self.particle_colors = particle_colors
        self.selected_colors = self.particle_colors[:self.number_of_colors]
        self.particle_size = particle_size
        self.particles = self.generate_random_particles()
        self.attraction_matrix = self.get_sample_matrix(2)
        self.current_demo_matrix = current_demo_matrix
        self.key_press = current_demo_matrix

        # Debug
        self.debug = debug

    def update(self):
        """
        Update particle canvas
        """
        self.engine.update()

    def update_matrix(self, matrix_number):
        """
        Update attraction matrix

        """
        self.attraction_matrix = self.get_sample_matrix(matrix_number)

    def update_particle_colors(self):
        """
        Update particle colors
        """
        self.selected_colors = self.particle_colors[:self.number_of_colors]
        self.update_particle_number()

    def update_particle_number(self):
        """
        Update total number of particles
        """
        self.particles_per_color = round(self.total_particles / self.number_of_colors)
        self.particles = self.generate_random_particles()

    def generate_random_particles(self):
        """
        Generate random particles for each color.
        Returns list of generatd particles
        """
        particles = []

        for color in self.selected_colors:
            for i in range(self.particles_per_color):
                x = random.uniform(self.UI_space, self.canvas_size['Width'] + self.UI_space)
                y = random.uniform(0, self.canvas_size['Height'])
                particles.append(particle.Particle(x, y, color))

        return particles

    def generate_random_matrix(self):
        """
        Generate random attraction matrix.
        Values are between -1 and 1
        """
        matrix = [[0 for x in range(len(self.particle_colors))] for y in range(len(self.particle_colors))]
        for i in range(len(self.particle_colors)):
            for j in range(len(self.particle_colors)):
                matrix[i][j] = round(random.uniform(-1, 1), 1)
        return matrix

    def get_sample_matrix(self, matrix_number):
        """
        Returns example attraction matrices
        """
        match matrix_number:
            # snake matrix. each color is attracted to the next color (1 to itself, 0.2 to the next color, 0 to the rest)
            case 1:
                matrix = [
                    [1, 0.2, 0, 0, 0, 0],
                    [0, 1, 0.2, 0, 0, 0],
                    [0, 0, 1, 0.2, 0, 0],
                    [0, 0, 0, 1, 0.2, 0],
                    [0, 0, 0, 0, 1, 0.2],
                    [0.2, 0, 0, 0, 0, 1]
                ]

            # random matrix but kinda fun
            case 2:
                matrix = [
                    [0.3, -0.5, -0.3, 0.3, 0.5, 0.3],
                    [1, 0.5, 1, 0.5, 0.3, 0.5],
                    [-0.5, 1, 0.5, -1, 0.5, 0.3],
                    [-0.3, 1, 0.5, 0.8, 0.5, 0.3],
                    [0.3, 0.5, 0.8, 0.5, 0.3, 0.5],
                    [0.5, 0.3, 0.5, 0.3, 0.5, 0.3]
                ]

            # chain matrix 1
            case 3:
                matrix = [
                    [1, 0.2, -1, -1, -1, 0.2],
                    [0.2, 1, 0.2, -1, -1, -1],
                    [-1, 0.2, 1, 0.2, -1, -1],
                    [-1, -1, 0.2, 1, 0.2, -1],
                    [-1, -1, -1, 0.2, 1, 0.2],
                    [0.2, -1, -1, -1, 0.2, 1]
                ]

            # chain matrix 2
            case 4:
                matrix = [
                    [1, 1, -1, -1, -1, 1],
                    [1, 1, 1, -1, -1, -1],
                    [-1, 1, 1, 1, -1, -1],
                    [-1, -1, 1, 1, 1, -1],
                    [-1, -1, -1, 1, 1, 1],
                    [1, -1, -1, -1, 1, 1]
                ]

                # chain matrix 3
            case 5:
                matrix = [
                    [1, 0.2, 0, 0, 0, 0.2],
                    [0.2, 1, 0.2, 0, 0, 0],
                    [0, 0.2, 1, 0.2, 0, 0],
                    [0, 0, 0.2, 1, 0.2, 0],
                    [0, 0, 0, 0.2, 1, 0.2],
                    [0.2, 0, 0, 0, 0.2, 1]
                ]

            # Write a loop that generates a random symmetric matrix
            # generate random symmetric matrix, split diagonally from top left to bottom right
            case 6:
                matrix = [
                    [
                        1 if i == j else round(random.uniform(-1, 1), 1)
                        for j in range(len(self.particle_colors))
                    ]
                    for i in range(len(self.particle_colors))
                ]
                for i in range(len(self.particle_colors)):
                    for j in range(len(self.particle_colors)):
                        if i > j:
                            matrix[i][j] = matrix[j][i]
            case _:
                matrix = self.generate_random_matrix()

        return matrix
