import engine
import window
import particle_canvas

import time



def main():
    # Create particle_canvas, window and engine objects
    cnvs = particle_canvas.ParticleCanvas(particlesPerColor = 50, colors = ['red', 'green', 'blue', 'orange'], border = False, canvasSize = {'Width': 1200, 'Height': 1200})
    wndw = window.Window(particle_canvas=cnvs, title='Particle Life', size = {'Width': 1200, 'Height': 1200}, background='black')
    eng = engine.Engine(cnvs)
    wndw.DrawParticles()

    # FPS counter
    start_time = time.time()
    counter = 0

    while True:
        eng.updateParticleVelocities()
        wndw.updateParticlePositions()
        wndw.window.update_idletasks()
        wndw.window.update()
        
        # FPS counter
        counter+=1
        if (time.time() - start_time) > 1 : # displays the frame rate every 1 second
            wndw.updateFPS(round(counter / (time.time() - start_time)))
            counter = 0
            start_time = time.time()
    

if __name__ == '__main__':
    main()