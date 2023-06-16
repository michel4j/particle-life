import pyglet
import particle_canvas
import window
import engine
import time

debug_state = True

cnvs = particle_canvas.ParticleCanvas(particles_per_color = 30, 
                                      colors = ['red', 'green', 'blue', 'orange'], 
                                      particle_size = 2, 
                                      canvas_border = False, 
                                      canvas_size = {'Width': 1000, 'Height': 1000},
                                      debug = debug_state)

wndw = window.Window(particle_canvas = cnvs, 
                     title = 'Particle Life', 
                     debug = debug_state)

eng = engine.Engine(particle_canvas = cnvs, 
                    debug = debug_state)

def game_loop(self):
    
    # For FPS calculation
    begin = time.time_ns()  / (10 ** 9) # convert to seconds

    # Update particle velocities
    eng.update()

    # Update particle positions on canvas
    cnvs.update()

    # Render pyglet window
    wndw.update()

    # Total time & FPS
    cycle_time = (time.time_ns()  / (10 ** 9)) - begin
    if debug_state:
        print("--------------------------------------------------------------------")
        print("Cycle time:\t\t\t\t\t" + str(cycle_time) + " seconds")
    if cycle_time == 0:
        wndw.updateFPS(round(1 / 0.01666))
        if debug_state:
            print("FPS:\t\t\t\t\t\t" + str(round(1 / 0.01666)) + "\n\n")
    else:
        wndw.updateFPS(round(1 / cycle_time))
        if debug_state:
            print("FPS:\t\t\t\t\t\t" + str(round(1 / cycle_time)) + "\n\n")

if __name__ == "__main__":
    pyglet.clock.schedule_interval(game_loop, 1/60.0)
    pyglet.app.run()
