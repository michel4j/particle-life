import pyglet
import color_to_RGB

class Window():
    
    def __init__(self, particle_canvas, title='Particle Life', size = {'Width': 1200, 'Height': 1200}):
        self.size = size
        self.title = title

        # Create window
        self.window = pyglet.window.Window(size['Width'], size['Height'], self.title)
        
        # Pyglet rendering
        self.batch = pyglet.graphics.Batch()
        self.vertex_list = None

        # Particle canvas
        self.particleCanvas = particle_canvas

        # Create FPS text
        self.fps_label = pyglet.text.Label("FPS: 000",
                        font_size=10,
                        x=32, y=self.window.height - 23,
                        anchor_x='center', anchor_y='center')

        # Create number of particles text
        number_of_particles = len(self.particleCanvas.particles)
        if number_of_particles < 10:
            particle_text = "Particles: 0000" + str(number_of_particles)
        elif number_of_particles < 100:
            particle_text = "Particles: 000" + str(number_of_particles)
        elif number_of_particles < 1000:
            particle_text = "Particles: 00" + str(number_of_particles)
        elif number_of_particles < 10000:
            particle_text = "Particles: 0" + str(number_of_particles)
        else:
            particle_text = "Particles: " + str(number_of_particles)
        self.particle_count_label = pyglet.text.Label(particle_text,
                        font_size=10,
                        x=54, y=self.window.height - 7,
                        anchor_x='center', anchor_y='center')

        # Create vertex list for particles
        vertices = []
        colors = []
        for prtcl in self.particleCanvas.particles:
            vertices.extend([prtcl.posX, prtcl.posY])
            colors.extend(color_to_RGB.transform(prtcl.color))
        self.vertex_list = self.batch.add(len(self.particleCanvas.particles), pyglet.gl.GL_POINTS, None,
                                                       ('v2f', vertices),
                                                       ('c3B', colors),)  

    def updateFPS(self, fps):
        if fps < 10:
            self.fps_label.text = "FPS: 00" + str(fps)
        elif fps < 100:
            self.fps_label.text = "FPS: 0" + str(fps)
        else:
            self.fps_label.text = "FPS: " + str(fps)

    def updateObjectPositions(self):	
        vertices = []
        for prtcl in self.particleCanvas.particles:
            # Update particle position in particle canvas
            self.particleCanvas.updateParticlePosition(prtcl)

            # Update particle position in pyglet window
            vertices.extend([prtcl.posX, prtcl.posY])

        self.vertex_list.vertices = vertices
