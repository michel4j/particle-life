import pyglet
import color_to_RGB
import time
from pyglet.window import key

class Window():
    
    def __init__(self, particle_canvas, title='Particle Life', debug = False):
        # Particle canvas object
        self.particle_canvas = particle_canvas
        
        # Create window
        self.window_size = {'Width': particle_canvas.canvas_size['Width'], 'Height': particle_canvas.canvas_size['Height']}
        self.title = title
        self.window = pyglet.window.Window(self.window_size['Width'] + particle_canvas.UI_space, self.window_size['Height'], self.title)
        
        # Pyglet rendering
        self.batch = pyglet.graphics.Batch()
        self.vertex_list = self.createNewVertexList()

        # UI Shit
        self.space_between_labels = 14
        self.font_size = 10 
        
        # Create number of particles label
        self.particle_count_label = pyglet.text.Label("Particles: " + str(len(self.particle_canvas.particles)),
                        font_size=self.font_size,
                        x=2, y=self.window.height - self.space_between_labels)
        
        # Create FPS label
        self.fps_label = pyglet.text.Label("FPS: ",
                         font_size=self.font_size,
                         x=2, y=self.particle_count_label.y - self.space_between_labels)
        
        # Create dt label
        self.dt_label = pyglet.text.Label("Time dt: " + str(self.particle_canvas.engine.dt), 
                        font_size=self.font_size,
                        x=2, y=self.fps_label.y - (self.space_between_labels * 2))

        # Create rMax label
        self.rMax_label = pyglet.text.Label("rMax: " + str(self.particle_canvas.engine.rMax), 
                        font_size=self.font_size,
                        x=2, y=self.dt_label.y - self.space_between_labels)
        
        # Create forceFactor label
        self.forceFactor_label = pyglet.text.Label("ForceFactor: " + str(self.particle_canvas.engine.forceFactor),
                        font_size=self.font_size,
                        x=2, y=self.rMax_label.y - self.space_between_labels)
        
        # Create frictionHalfLife label
        self.frictionHalfLife_label = pyglet.text.Label("FrictionHalfLife: " + str(self.particle_canvas.engine.frictionHalfLife),
                        font_size=self.font_size,
                        x=2, y=self.forceFactor_label.y - self.space_between_labels)
        
        # Create frictionFactor label
        self.frictionFactor_label = pyglet.text.Label("FrictionFactor: " + str(round(self.particle_canvas.engine.frictionFactor, 3)),
                        font_size=self.font_size,
                        x=2, y=self.frictionHalfLife_label.y - self.space_between_labels)

        @self.window.event
        def on_key_press(symbol, modifiers):
            
            # change particle count on key press
            if symbol == key.Q:
                self.particle_canvas.total_particles += 1000
                self.particle_canvas.updateParticleNumber()
                # Clear old batch and create new vertex list and add it to batch
                self.batch = pyglet.graphics.Batch()
                self.vertex_list = self.createNewVertexList()
                self.particle_count_label.text = "Particles: " + str(len(self.particle_canvas.particles))
            elif symbol == key.A:
                if self.particle_canvas.total_particles > 1000:
                    self.particle_canvas.total_particles -= 1000
                    self.particle_canvas.updateParticleNumber()
                    # Clear old batch and create new vertex list and add it to batch
                    self.batch = pyglet.graphics.Batch()
                    self.vertex_list = self.createNewVertexList()
                    self.particle_count_label.text = "Particles: " + str(len(self.particle_canvas.particles))

            # change dt on key press
            elif symbol == key.W:
                self.particle_canvas.engine.dt += 0.001
                self.dt_label.text = "Time dt: " + str(self.particle_canvas.engine.dt)
            elif symbol == key.S:
                self.particle_canvas.engine.dt -= 0.001
                self.dt_label.text = "Time dt: " + str(self.particle_canvas.engine.dt)

        self.debug = debug
    
    def update(self):
        """ Update window """
        if(self.debug):
            begin = time.time_ns()  / (10 ** 9)
        
        self.window.clear()
        
        # Particles
        self.updateObjectPositions()
        self.batch.draw()

        # UI
        self.particle_count_label.draw()
        self.fps_label.draw()
        self.dt_label.draw()
        self.rMax_label.draw()
        self.forceFactor_label.draw()
        self.frictionHalfLife_label.draw()
        self.frictionFactor_label.draw()


        if(self.debug):
            print("2. Render pyglet window:\t\t\t" + str(time.time_ns()  / (10 ** 9) - begin) + " seconds")
        
    def createNewVertexList(self):
        vertices, colors = self.updateVertexList()
        return self.batch.add(len(self.particle_canvas.particles) * 4, pyglet.gl.GL_QUADS, None,
                                                       ('v2f', vertices),
                                                       ('c3B', colors),) 

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

    def updateFPS(self, fps):
        """ Update FPS label """	
        self.fps_label.text = "FPS: " + str(fps)

    def updateObjectPositions(self):	
        """ Update vertex list for particles """
        self.vertex_list.vertices = self.updateVertexList(color=False)
