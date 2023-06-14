import pyglet
import color_to_RGB

class Window():
    
    def __init__(self, particle_canvas, title='Particle Life', size = {'Width': 1200, 'Height': 1200}):
        self.size = size
        self.title = title

        # Create window
        self.window = pyglet.window.Window(size['Width'], size['Height'], self.title)
        self.batch = pyglet.graphics.Batch()
        self.objects = []

        # Particle canvas
        self.particleCanvas = particle_canvas

        # Create FPS text
        self.fps_label = pyglet.text.Label("FPS: 000",
                        font_size=10,
                        x=28, y=self.window.height - 23,
                        anchor_x='center', anchor_y='center')

        # Create number of particles text
        number_of_particles = len(self.particleCanvas.particles)
        if number_of_particles < 10:
            particle_text = "Particles: 000" + str(number_of_particles)
        elif number_of_particles < 100:
            particle_text = "Particles: 00" + str(number_of_particles)
        elif number_of_particles < 1000:
            particle_text = "Particles: 0" + str(number_of_particles)
        else:
            particle_text = "Particles: " + str(number_of_particles)
        self.particle_count_label = pyglet.text.Label(particle_text,
                        font_size=10,
                        x=45, y=self.window.height - 7,
                        anchor_x='center', anchor_y='center')

        # Draw all particles
        for prtcl in self.particleCanvas.particles:
            temp = pyglet.shapes.Circle(x=prtcl.posX, y=prtcl.posY, radius=prtcl.size, color=color_to_RGB.transform(prtcl.color), batch=self.batch)
            self.objects.append(temp)

    def updateFPS(self, fps):
        if fps < 10:
            self.fps_label.text = "FPS: 00" + str(fps)
        elif fps < 100:
            self.fps_label.text = "FPS: 0" + str(fps)
        else:
            self.fps_label.text = "FPS: " + str(fps)

    def updateParticlePositions(self):
        for prtcl in self.particleCanvas.particles:
            dynamicObject = self.particleCanvas.particles.index(prtcl)

            if(self.particleCanvas.border):
                # revert velocity if particle is out of bounds
                prtcl.posX += prtcl.velX
                if prtcl.posX > self.particleCanvas.canvasSize['Width'] or prtcl.posX < 0:
                    prtcl.posX -= prtcl.velX

                prtcl.posY += prtcl.velY
                if prtcl.posY > self.particleCanvas.canvasSize['Height'] or prtcl.posY < 0:
                    prtcl.posY -= prtcl.velY
            else:
                # wrap particle around canvas if out of bounds
                prtcl.posX += prtcl.velX
                if prtcl.posX > self.particleCanvas.canvasSize['Width']:
                    prtcl.posX = 0
                
                if prtcl.posX < 0:
                    prtcl.posX = self.particleCanvas.canvasSize['Width']

                prtcl.posY += prtcl.velY
                if prtcl.posY > self.particleCanvas.canvasSize['Height']:
                    prtcl.posY = 0

                if prtcl.posY < 0:
                    prtcl.posY = self.particleCanvas.canvasSize['Height']

            self.objects[dynamicObject].x = prtcl.posX
            self.objects[dynamicObject].y = prtcl.posY