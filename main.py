import pyglet
import particle_canvas
import window
import engine
import time

debug_state = True

cnvs = particle_canvas.ParticleCanvas(particles_per_color = 30, 
                                      particle_colors = ['red', 'green', 'blue', 'orange'], 
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
    
    # For cycle_time calculation
    begin = time.time_ns()  / (10 ** 9) # convert to seconds

    # Update particle velocities
    eng.update()

    # Update particle positions on canvas
    cnvs.update()

    # Render pyglet window
    wndw.update()

    # Calculate cycle time
    global cycle_time
    cycle_time = (time.time_ns()  / (10 ** 9)) - begin

    # Print cycle time and FPS
    if debug_state:
        print("--------------------------------------------------------------------")
        print("Cycle time:\t\t\t\t\t" + str(cycle_time) + " seconds")
        if cycle_time == 0:
            print("FPS:\t\t\t\t\t\t" + str(round(1 / 0.01666)) + "\n\n")
        else:
            print("FPS:\t\t\t\t\t\t" + str(round(1 / cycle_time)) + "\n\n")

def update_FPS_label(self):
    # Prevent division by zero
    if cycle_time == 0:
        fps = round(1 / 0.01666)
    else:
        fps = round(1 / cycle_time)

    wndw.updateFPS(fps)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(game_loop, 1/60.0) # update game loop 60 times per second
    pyglet.clock.schedule_interval(update_FPS_label, 1) # update FPS label every second
    pyglet.app.run()
