import pyglet
import color_to_RGB

class Window():
    
    def __init__(self, particle_canvas, title='Particle Life'):
        # Create window
        self.window_size = {'Width': particle_canvas.canvas_size['Width'], 'Height': particle_canvas.canvas_size['Height']}
        self.title = title
        self.window = pyglet.window.Window(self.window_size['Width'], self.window_size['Height'], self.title)
        
        # Pyglet rendering
        self.batch = pyglet.graphics.Batch()
        self.vertex_list = None

        # Particle canvas
        self.particle_canvas = particle_canvas

        # Create FPS label
        self.fps_label = pyglet.text.Label("FPS: 000",
                        font_size=10,
                        x=32, y=self.window.height - 23,
                        anchor_x='center', anchor_y='center')

        # Create number of particles label
        self.particle_count_label = pyglet.text.Label(self.numberOfParticlesText(),
                        font_size=10,
                        x=54, y=self.window.height - 7,
                        anchor_x='center', anchor_y='center')

        # Create vertex list for particles -> quads
        vertices = []
        colors = []
        for prtcl in self.particle_canvas.particles:
            vertices.extend([prtcl.posX                                     , prtcl.posY                                    ,
                             prtcl.posX                                     , prtcl.posY +self.particle_canvas.particle_size,
                             prtcl.posX +self.particle_canvas.particle_size , prtcl.posY +self.particle_canvas.particle_size,
                             prtcl.posX +self.particle_canvas.particle_size , prtcl.posY                                    ])
            colors.extend(color_to_RGB.transform(prtcl.color) * 4)
        self.vertex_list = self.batch.add(len(self.particle_canvas.particles) * 4, pyglet.gl.GL_QUADS, None,
                                                       ('v2f', vertices),
                                                       ('c3B', colors),)  

    def numberOfParticlesText(self):
        number_of_particles = len(self.particle_canvas.particles)
        if number_of_particles < 10:
            return "Particles: 0000" + str(number_of_particles)
        elif number_of_particles < 100:
            return "Particles: 000" + str(number_of_particles)
        elif number_of_particles < 1000:
            return "Particles: 00" + str(number_of_particles)
        elif number_of_particles < 10000:
            return "Particles: 0" + str(number_of_particles)
        else:
            return "Particles: " + str(number_of_particles)

    def updateFPS(self, fps):
        if fps < 10:
            self.fps_label.text = "FPS: 00" + str(fps)
        elif fps < 100:
            self.fps_label.text = "FPS: 0" + str(fps)
        else:
            self.fps_label.text = "FPS: " + str(fps)

    def updateObjectPositions(self):	
        vertices = []
        for prtcl in self.particle_canvas.particles:
            # Update particle position in particle canvas
            self.particle_canvas.updateParticlePosition(prtcl)

            # Update particle position in pyglet window

            vertices.extend([prtcl.posX                                     , prtcl.posY                                    ,
                             prtcl.posX                                     , prtcl.posY +self.particle_canvas.particle_size,
                             prtcl.posX +self.particle_canvas.particle_size , prtcl.posY +self.particle_canvas.particle_size,
                             prtcl.posX +self.particle_canvas.particle_size , prtcl.posY                                    ])
        self.vertex_list.vertices = vertices
