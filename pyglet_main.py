import pyglet
import particle_canvas
import pyglet_window
import engine

cnvs = particle_canvas.ParticleCanvas(particlesPerColor = 20, colors = ['red', 'green', 'blue', 'orange'], border = False, canvasSize = {'Width': 1200, 'Height': 1200})
wndw = pyglet_window.Window(particle_canvas=cnvs, title='Particle Life', size = {'Width': 1200, 'Height': 1200})
eng = engine.Engine(cnvs)

@wndw.window.event
def on_draw():
    wndw.window.clear()
    wndw.particle_count_label.draw()
    wndw.batch.draw()
    wndw.fps_display.draw()


def update(dt):
    eng.updateParticleVelocities()
    wndw.updateParticlePositions()

pyglet.clock.schedule_interval(update, 1/60.0)

pyglet.app.run()