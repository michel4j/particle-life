import particle
from tkinter import Tk, Frame, Canvas

def main():
    window=Tk()
    
    canvas = Canvas(width=800, height=800, background='black')
    canvas.pack()

    particles = []

    particles.append(particle.Particle(50, 50, "red"))
    particles.append(particle.Particle(20, 20, "blue"))
    particles.append(particle.Particle(100, 200, "yellow"))
    particles.append(particle.Particle(700, 700, "green"))
    particles.append(particle.Particle(500, 500, "purple"))

    for prtcl in particles:
        canvas.create_oval(prtcl.posX, prtcl.posY, prtcl.posX + prtcl.size, prtcl.posY + prtcl.size, fill=prtcl.color)

    window.title('Particle Life')
    window.geometry("800x800")
    window.configure(background='white')
    window.mainloop()
    

if __name__ == '__main__':
    main()