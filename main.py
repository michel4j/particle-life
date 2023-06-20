import pyglet
import particle_canvas
import window
import time
from pynput.keyboard import Key, Controller
import random
keyboard = Controller()

debug_state = False

Particle_Canvas = particle_canvas.ParticleCanvas(total_particles = 10000, 
                                                 particle_colors = ['red', 'orange', 'yellow', 'light green', 'light blue', 'dark purple'], 
                                                 number_of_colors = 4,
                                                 particle_size = 2, 
                                                 canvas_border = False, 
                                                 canvas_size = {'Width': 1200, 'Height': 1200},
                                                 current_demo_matrix = 0,
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
    if Window.debug:
        print("--------------------------------------------------------------------")
        print("Cycle time:\t\t\t\t\t" + str(cycle_time) + " seconds")
        print("FPS:\t\t\t\t\t\t" + str(fps) + "\n\n")

def update_FPS_label(self):
    Window.updateFPS(fps)

def demo_mode(self):
    if Window.demo_mode == 0:
        pass
    elif Window.demo_mode == 1:
        Particle_Canvas.attraction_matrix = Particle_Canvas.returnExampleAttractionMatrices(0)
    elif Window.demo_mode == 2:
        # generate random (seed with time) number between 0 and 6
        random.seed(time.time_ns())
        random_number = random.randint(0, 6)
        keyboard.press(str(random_number))
        keyboard.release(str(random_number)) 
    else:
        # Change current demo matrix in this order: 0 -> 1 -> 0 -> 2 -> 0 -> 3 -> 0 -> 4 -> 0 -> 5 and loop
        keyboard.press(str(Particle_Canvas.key_press))
        keyboard.release(str(Particle_Canvas.key_press)) 
        if Particle_Canvas.key_press == 0:
            Particle_Canvas.current_demo_matrix = (Particle_Canvas.current_demo_matrix + 1) % 6
            Particle_Canvas.key_press = Particle_Canvas.current_demo_matrix
        else:
            Particle_Canvas.key_press = 0


if __name__ == "__main__":
    pyglet.clock.schedule_interval(game_loop, 1/60.0) # update game loop 60 times per second
    pyglet.clock.schedule_interval(update_FPS_label, 1) # update FPS label every second
    pyglet.clock.schedule_interval(demo_mode, 15) # update demo mode every 5 seconds
    fps = 0 # initialize FPS just in case it is not updated in the first second
    pyglet.app.run()
