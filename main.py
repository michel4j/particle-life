import engine
import window
import particle_canvas

import time



def main():
    # Create particle_canvas, window and engine objects
    cnvs = particle_canvas.ParticleCanvas(particlesPerColor = 50, colors = ['red', 'green', 'blue', 'orange'], border = False, canvasSize = {'Width': 1200, 'Height': 1200})
    wndw = window.Window(particle_canvas=cnvs, title='Particle Life', size = {'Width': 1200, 'Height': 1200}, background='black')
    eng = engine.Engine(cnvs)
    wndw.DrawParticles()

    # FPS counter
    start_time = time.time()
    counter = 0

    while True:
        begin = time.time()

        eng.updateParticleVelocities()
        time_elapsed = time.time() - begin
        print("1. calculate forces between particles:  " + str(time_elapsed) + " seconds")

        wndw.updateParticlePositions()
        time_elapsed = time.time() - time_elapsed - begin
        print("2. move particles: \t\t\t" + str(time_elapsed) + " seconds")
 
        wndw.window.update_idletasks()
        wndw.window.update()
        time_elapsed = time.time() - time_elapsed - begin
        print("3. update window:\t\t\t" + str(time_elapsed) + " seconds\n")
        
        # FPS counter
        counter+=1
        if (time.time() - start_time) > 1 : # displays the frame rate every 1 second
            wndw.updateFPS(round(counter / (time.time() - start_time)))
            counter = 0
            start_time = time.time()
        
        # FPS limit to 60
        cycle = time.time() - begin
        print("cycle time: " + str(cycle))
        if (time.time() - begin) < 0.01666: # 60is fps
            delay = (0.01666 - (time.time() - begin)) / 2  # dont ask why dividing by 2 solves the problem. Sleep is not accurate
            print("Delay: " + str(delay))
            print("Combined time: " + str(delay + cycle))
            time.sleep(delay)

        actual_total_time = time.time() - begin
        print("Total time per loop: " + str(actual_total_time) + "\n\n")
    

if __name__ == '__main__':
    main()