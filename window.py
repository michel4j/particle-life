import pyglet
import color_to_RGB
import time

class Window():
    
    def __init__(self, particle_canvas, title='Particle Life', debug = False):
        # Create window
        self.window_size = {'Width': particle_canvas.canvas_size['Width'], 'Height': particle_canvas.canvas_size['Height']}
        self.title = title
        self.window = pyglet.window.Window(self.window_size['Width'], self.window_size['Height'], self.title)
        
        # Pyglet rendering
        self.batch = pyglet.graphics.Batch()
        self.vertex_list = None

        self.debug = debug

        # Particle canvas
        self.particle_canvas = particle_canvas

        # Create FPS label
        self.fps_label = pyglet.text.Label("FPS: 0000",
                        font_size=10,
                        x=36, y=self.window.height - 23,
                        anchor_x='center', anchor_y='center')

        # Create number of particles label
        self.particle_count_label = pyglet.text.Label(self.numberOfParticlesText(),
                        font_size=10,
                        x=54, y=self.window.height - 7,
                        anchor_x='center', anchor_y='center')

        # Create vertex list for particles(use GL_QUADS)
        vertices, colors = self.updateVertexList()
        self.vertex_list = self.batch.add(len(self.particle_canvas.particles) * 4, pyglet.gl.GL_QUADS, None,
                                                       ('v2f', vertices),
                                                       ('c3B', colors),)  
    
    def update(self):
        """ Update window """
        if(self.debug):
            begin = time.time_ns()  / (10 ** 9)
        
        self.window.clear()
        self.updateObjectPositions()
        self.batch.draw()
        self.particle_count_label.draw()
        self.fps_label.draw()

        if(self.debug):
            print("3. Render pyglet window:\t\t\t" + str(time.time_ns()  / (10 ** 9) - begin) + " seconds")
        

    def updateVertexList(self, color=True):
        """ Create vertex list for particles. 
        Option to also create color list """	
        vertices = []
        colors = []
        for prtcl in self.particle_canvas.particles:
            vertices.extend([prtcl.posX                                     , prtcl.posY                                    ,
                             prtcl.posX                                     , prtcl.posY +self.particle_canvas.particle_size,
                             prtcl.posX +self.particle_canvas.particle_size , prtcl.posY +self.particle_canvas.particle_size,
                             prtcl.posX +self.particle_canvas.particle_size , prtcl.posY                                    ])
            if(color):
                colors.extend(color_to_RGB.transform(prtcl.color) * 4)
        
        if(color):
            return vertices, colors
        else:
            return vertices

    def numberOfParticlesText(self):
        """ Returns text for number of particles label """	
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
        """ Update FPS label """	
        if fps < 10:
            self.fps_label.text = "FPS: 000" + str(fps)
        elif fps < 100:
            self.fps_label.text = "FPS: 00" + str(fps)
        elif fps < 1000:
            self.fps_label.text = "FPS: 0" + str(fps)
        else:
            self.fps_label.text = "FPS: " + str(fps)

    def updateObjectPositions(self):	
        """ Update vertex list for particles """
        self.vertex_list.vertices = self.updateVertexList(color=False)
