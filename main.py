import engine
import window
import particle_canvas

import time
def sleep(duration, get_now=time.perf_counter):
    now = get_now()
    end = now + duration
    while now < end:
        now = get_now()

def main():
    # Create particle_canvas, window and engine objects
    cnvs = particle_canvas.ParticleCanvas(particlesPerColor = 2500, colors = ['red', 'green', 'blue', 'orange'], border = False, canvasSize = {'Width': 1200, 'Height': 1200})
    wndw = window.Window(particle_canvas=cnvs, title='Particle Life', size = {'Width': 1200, 'Height': 1200}, background='black')
    eng = engine.Engine(cnvs)
    wndw.DrawParticles()

    # FPS counter
    start_time = time.time()
    counter = 0

    while True:
        begin = time.time()

        #eng.updateParticleVelocities()
        time_elapsed_force = time.time() - begin
        print("1. Calculate forces between particles:\t" + str(time_elapsed_force) + " seconds")

        wndw.updateParticlePositions()
        time_elapsed_move = time.time() - time_elapsed_force - begin
        print("2. Adjust particle coordinates: \t" + str(time_elapsed_move) + " seconds")
 
        wndw.window.update_idletasks()
        wndw.window.update()
        time_elapsed_update = time.time() - time_elapsed_force - time_elapsed_move - begin
        print("3. Update window and render window:\t" + str(time_elapsed_update) + " seconds")
        
        # FPS counter
        counter+=1
        if (time.time() - start_time) > 1 : # displays the frame rate every 1 second
            wndw.updateFPS(round(counter / (time.time() - start_time)))
            counter = 0
            start_time = time.time()
        
        # FPS limit to 60
        cycle_time = time.time() - begin
        print("--------------------------------------------------------------------")
        print("Cycle time:\t\t\t\t" + str(cycle_time) + " seconds")
        if cycle_time < 0.015: # 60is fps
            delay = (0.01666 - (time.time() - begin)) # dont ask why dividing by 1.2 solves the problem
            print("added delay of:\t\t\t\t" + str(delay) + " seconds")
            sleep(delay)

        actual_total_time = time.time() - begin
        print("\nTotal time per loop:\t\t\t" + str(actual_total_time) + " seconds")
        if actual_total_time != 0:
            print("FPS:\t\t\t\t\t" + str(round(1 / actual_total_time)) + "\n\n")
    

if __name__ == '__main__':
    main()

