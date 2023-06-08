import engine
import window
import particle_canvas

import time

def main():
    cnvs = particle_canvas.ParticleCanvas(particlesPerColor = 50, colors = ['red', 'green', 'blue', 'orange'], border = False, canvasSize = {'Width': 1200, 'Height': 1200})
    wndw = window.Window(particle_canvas=cnvs, title='Particle Life', size = {'Width': 1200, 'Height': 1200}, background='black')
    eng = engine.Engine(cnvs)
    wndw.DrawParticles()

    while True:
        eng.updateParticleVelocities()
        wndw.updateParticlePositions()
        wndw.window.update_idletasks()
        wndw.window.update()
        time.sleep(eng.dt)
    

if __name__ == '__main__':
    main()