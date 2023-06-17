import pyglet
import particle_canvas
import window
import time

debug_state = False

Particle_Canvas = particle_canvas.ParticleCanvas(total_particles = 10000, 
                                                 particle_colors = ['red', 'blue', 'green', 'purple'], 
                                                 particle_size = 2, 
                                                 canvas_border = False, 
                                                 canvas_size = {'Width': 1200, 'Height': 1200},
                                                 debug = debug_state)

Window = window.Window(particle_canvas = Particle_Canvas, 
                       title = 'Particle Life', 
                       debug = debug_state)

def game_loop(self):
    
    # For cycle_time calculation
    begin = time.time_ns()  / (10 ** 9) # convert to seconds

    # Update particles on canvas
    Particle_Canvas.update()

    # Render pyglet window
    Window.update()

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
    Window.updateFPS(fps)

if __name__ == "__main__":
    pyglet.clock.schedule_interval(game_loop, 1/60.0) # update game loop 60 times per second
    pyglet.clock.schedule_interval(update_FPS_label, 1) # update FPS label every second
    fps = 0 # initialize FPS just in case it is not updated in the first second
    pyglet.app.run()
