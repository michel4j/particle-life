import random
import time

import pyglet
from pynput.keyboard import Controller

import canvas
import window

keyboard = Controller()
debug_state = False

particle_canvas = canvas.ParticleCanvas(
    total_particles=20000,
    particle_colors=['red', 'orange', 'yellow', 'light green', 'light blue', 'dark purple'],
    number_of_colors=4,
    particle_size=1,
    canvas_border=False,
    canvas_size={'Width': 900, 'Height': 900},
    current_demo_matrix=0,
    debug=debug_state
)

Window = window.Window(
    particle_canvas=particle_canvas,
    title='Particle Life',
    debug=debug_state
)


def game_loop(self):
    # For cycle_time calculation
    begin_ns = time.time_ns()

    # Update particles on canvas
    particle_canvas.update()

    # Render pyglet window
    Window.update()

    # Calculate cycle time
    cycle_time_ns = time.time_ns() - begin_ns
    cycle_time = cycle_time_ns / 1000000000

    # Update FPS when cycle time is not zero
    global fps
    if cycle_time != 0:
        fps = round(1 / cycle_time)

    # Print cycle time and FPS
    if Window.debug:
        print("--------------------------------------------------------------------")
        print("Cycle time:\t\t\t\t\t" + str(cycle_time) + " seconds")
        print("FPS:\t\t\t\t\t\t" + str(fps) + "\n\n")


def update_fps_label(self):
    Window.update_fps(fps)


def demo_mode(self):
    # Demo mode off
    if Window.demo_mode == 0:
        pass

    # Demo mode random matrices
    elif Window.demo_mode == 1:
        particle_canvas.update_matrix(0)

    # Demo mode random example matrices
    elif Window.demo_mode == 2:
        # generate random (seed with time) number between 0 and 6
        random.seed(time.time_ns())
        random_number = random.randint(0, 6)
        keyboard.press(str(random_number))
        keyboard.release(str(random_number))

        # Demo mode example matrices in set order
    else:
        # Change current demo matrix in this order: 0 -> 1 -> 0 -> 2 -> 0 -> 3 -> 0 -> 4 -> 0 -> 5 and loop
        keyboard.press(str(particle_canvas.key_press))
        keyboard.release(str(particle_canvas.key_press))
        if particle_canvas.key_press == 0:
            particle_canvas.current_demo_matrix = (particle_canvas.current_demo_matrix + 1) % 6
            particle_canvas.key_press = particle_canvas.current_demo_matrix
        else:
            particle_canvas.key_press = 0


if __name__ == "__main__":
    pyglet.clock.schedule_interval(game_loop, 1 / 60.0)  # update game loop 60 times per second
    pyglet.clock.schedule_interval(update_fps_label, 1)  # update FPS label every second
    pyglet.clock.schedule_interval(demo_mode, 15)  # update demo mode every 5 seconds
    fps = 0  # initialize FPS just in case it is not updated in the first second
    pyglet.app.run()
