from tkinter import Tk, Canvas, Label, StringVar

class Window():
    
    def __init__(self, particle_canvas, title='Particle Life', size = {'Width': 1200, 'Height': 1200}, background='black'):
        self.size = size
        self.title = title
        self.backgrond = background

        # Create window
        self.window=Tk()
        self.window.title(title)

        # Create canvas 
        self.canvas = Canvas(width=size['Width'], height=size['Height'], bg=background)
        self.canvas.pack()

        # Create FPS text
        self.fps_label = Label(self.canvas, text = "FPS: 000", font=('serif', 10, 'bold'))
        self.fps_label.config(bg='black', fg='white')
        self.fps_label.pack()
        self.canvas.create_window(32, 30, window=self.fps_label)

        # Particle canvas
        self.particleCanvas = particle_canvas

        # Create particle count text
        number_of_particles = len(self.particleCanvas.particles)
        if number_of_particles < 10:
            particle_text = "Particles: 000" + str(number_of_particles)
        elif number_of_particles < 100:
            particle_text = "Particles: 00" + str(number_of_particles)
        elif number_of_particles < 1000:
            particle_text = "Particles: 0" + str(number_of_particles)
        else:
            particle_text = "Particles: " + str(number_of_particles)
        self.particle_count_label = Label(self.canvas, text = particle_text, font=('serif', 10, 'bold'))
        self.particle_count_label.config(bg='black', fg='white')
        self.particle_count_label.pack()
        self.canvas.create_window(50, 13, window=self.particle_count_label)

    def updateFPS(self, fps):
        if fps < 10:
            self.fps_label.config(text="FPS: 00" + str(fps))
        elif fps < 100:
            self.fps_label.config(text="FPS: 0" + str(fps))
        else:
            self.fps_label.config(text="FPS: " + str(fps))
    
    def updateParticlePositions(self):
        object = 3 # 1 is fps tex, 2 is particle count text
        for prtcl in self.particleCanvas.particles:
            
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

            self.canvas.moveto(object, prtcl.posX, prtcl.posY)
            object += 1
        
    def DrawParticles(self):
        for prtcl in self.particleCanvas.particles:
            self.canvas.create_oval(prtcl.posX, prtcl.posY, prtcl.posX + prtcl.size, prtcl.posY + prtcl.size, fill=prtcl.color)
