import pyglet
import particle_canvas
import window
import engine
import time

debug_state = True

cnvs = particle_canvas.ParticleCanvas(particles_per_color = 1, 
                                      particle_colors = ['red', 'green', 'blue', 'orange'], 
                                      particle_size = 5, 
                                      canvas_border = False, 
                                      canvas_size = {'Width': 1200, 'Height': 1200},
                                      debug = debug_state)

wndw = window.Window(particle_canvas = cnvs, 
                     title = 'Particle Life', 
                     debug = debug_state)

eng = engine.Engine(particle_canvas = cnvs, 
                    debug = debug_state)

def game_loop(self):
    
    # For cycle_time calculation
    begin = time.time_ns()  / (10 ** 9) # convert to seconds

    # Update particle velocities
    eng.update()

    # Update particle positions on canvas
    cnvs.update()

    # Render pyglet window
    wndw.update()

    # Calculate cycle time
    cycle_time = (time.time_ns()  / (10 ** 9)) - begin

    # Update FPS when cycle time is not zero
    global fps
    if cycle_time != 0:
        fps = round(1 / cycle_time)

    # Print cycle time and FPS
    if debug_state:
        print("--------------------------------------------------------------------")
        print("Cycle time:\t\t\t\t\t" + str(cycle_time) + " seconds")
        print("FPS:\t\t\t\t\t\t" + str(fps) + "\n\n")

def update_FPS_label(self):
    wndw.updateFPS(fps)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(game_loop, 1/60.0) # update game loop 60 times per second
    pyglet.clock.schedule_interval(update_FPS_label, 1) # update FPS label every second
    fps = 0 # initialize FPS just in case it is not updated in the first second
    pyglet.app.run()
