import pyglet
import particle_canvas
import window
import engine
import time

cnvs = particle_canvas.ParticleCanvas(particles_per_color = 50, 
                                      colors = ['red', 'green', 'blue', 'orange'], 
                                      particle_size = 2, 
                                      canvas_border = False, 
                                      canvas_size = {'Width': 1000, 'Height': 1000})

wndw = window.Window(particle_canvas=cnvs, title='Particle Life')
eng = engine.Engine(cnvs)

def update(dt):
    begin = time.time()
    
    # Clear window
    wndw.window.clear()

    # Update particle velocities
    eng.updateParticleVelocities()
    time_elapsed_force = time.time() - begin
    print("1. Calculate forces between particles:\t" + str(time_elapsed_force) + " seconds")

    # Update particle positions
    cnvs.update()
    time_elapsed_move = time.time() - time_elapsed_force - begin
    print("2. Adjust particle coordinates: \t" + str(time_elapsed_move) + " seconds")

    # Render particles
    wndw.update()
    wndw.batch.draw()
    time_elapsed_update = time.time() - time_elapsed_force - time_elapsed_move - begin
    print("3. Update window and render window:\t" + str(time_elapsed_update) + " seconds")
    
    # Draw text
    wndw.particle_count_label.draw()
    wndw.fps_label.draw()

    # Total time & FPS
    cycle_time = time.time() - begin
    print("--------------------------------------------------------------------")
    print("Cycle time:\t\t\t\t" + str(cycle_time) + " seconds")
    if cycle_time > 0:
        wndw.updateFPS(round(1 / cycle_time))
        print("FPS:\t\t\t\t\t" + str(round(1 / cycle_time)) + "\n\n")

pyglet.clock.schedule_interval(update, 1/60.0)

if __name__ == "__main__":
    pyglet.app.run()
