import globals
import engine
import window

from tkinter import Tk, Frame, Canvas
import time

def main():
    global wndw
    wndw = window.Window()
    window.Window.DrawParticles()

    while True:
        update()
        wndw.window.update_idletasks()
        wndw.window.update()
        time.sleep(globals.dt)
    
def update():
    engine.Engine.updateParticleVelocities()
    window.Window.updateParticlePositions()

if __name__ == '__main__':
    main()