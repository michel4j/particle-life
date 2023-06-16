import math
import time
import pyopencl as cl
import numpy as np



class Engine():
    def __init__(self, particle_canvas, debug = False):
        # Time
        self.dt = 0.02

        # Particles 
        self.rMax = 250
        self.frictionHalfLife = 0.04
        self.frictionFactor = math.pow(0.5, self.dt / self.frictionHalfLife)
        self.forceFactor = 0.5
        
        # Canvas
        self.particle_canvas = particle_canvas

        # Pyopencl 
        self.platform = cl.get_platforms()[0]
        self.device = self.platform.get_devices()[0]
        self.context = cl.Context([self.device])
        self.queue = cl.CommandQueue(self.context)

        self.program = cl.Program(self.context, self.kernelCode()).build()

        self.debug = debug

    def update(self, opencl = True):
        """ Update particle velocities """
        if(self.debug):
            begin = time.time_ns()  / (10 ** 9)
        
        if(opencl):
            print("Particle[0] X velocity before: " + str(self.particle_canvas.particles[0].velX))
            print("Particle[0] X position before: " + str(self.particle_canvas.particles[0].posX))
            self.pyopenclUpdateParticleVelocities()
            for prtcl in self.particle_canvas.particles:
                self.updateParticlePosition(prtcl)
            print("Particle[0] X velocity after: " + str(self.particle_canvas.particles[0].velX))
            print("Particle[0] X position after: " + str(self.particle_canvas.particles[0].posX))
        else:
            print("Particle[0] X velocity before: " + str(self.particle_canvas.particles[0].velX))
            print("Particle[0] X position before: " + str(self.particle_canvas.particles[0].posX))
            self.updateParticleVelocities()
            print("Particle[0] X velocity after: " + str(self.particle_canvas.particles[0].velX))
            print("Particle[0] X position after: " + str(self.particle_canvas.particles[0].posX))

        if(self.debug):
            print("1. Calculate forces between particles:\t\t" + str(time.time_ns()  / (10 ** 9) - begin) + " seconds")

    def kernelCode(self):
        return"""
        // Kernel code
        float force(float r, float a) {
            float beta = 0.3;
            if (r < beta) {
                return r / beta - 1;
            } else if (beta < r && r < 1) {
                return a * (1 - fabs(2 * r - 1 - beta) / (1 - beta));
            } else {
                return 0;
            }
        }

        __kernel void updateParticleVelocities(__global float* positions,
                                            __global float* velocities,
                                            __global int* colors,
                                            int numParticles,
                                            float rMax,
                                            float forceFactor,
                                            float frictionFactor,
                                            float dt,
                                            float canvasWidth,
                                            float canvasHeight,
                                            __global float* attractionMatrix) {
            int gid = get_global_id(0);

            float totalForceX = 0;
            float totalForceY = 0;

            float prtclX = positions[2*gid];
            float prtclY = positions[2*gid + 1];
            int prtclColorIndex = colors[gid];

            for (int i = 0; i < numParticles; i++) {
                if (i == gid)
                    continue;

                float otherPrtclX = positions[2*i];
                float otherPrtclY = positions[2*i + 1];
                int otherPrtclColorIndex = colors[i];

                // Calculate distance between particles
                float rx = otherPrtclX - prtclX;
                float ry = otherPrtclY - prtclY;

                // Adjust for screen wrapping
                if (fabs(rx) > canvasWidth / 2) {
                    rx = canvasWidth - fabs(rx);
                }
                if (fabs(ry) > canvasHeight / 2) {
                    ry = canvasHeight - fabs(ry);
                }

                float r = sqrt(rx * rx + ry * ry);

                // Check if distance is greater than 0 and less than rMax
                if (r > 0 && r < rMax) {
                    float a = attractionMatrix[prtclColorIndex * numParticles + otherPrtclColorIndex];
                    float f = force(r / rMax, a);
                    totalForceX += f * rx / r;
                    totalForceY += f * ry / r;
                }
            }

            totalForceX *= rMax * forceFactor;
            totalForceY *= rMax * forceFactor;

            float velocityX = velocities[2*gid];
            float velocityY = velocities[2*gid + 1];

            velocityX *= frictionFactor;
            velocityY *= frictionFactor;

            velocityX += totalForceX * dt;
            velocityY += totalForceY * dt;

            velocities[2*gid] = velocityX;
            velocities[2*gid + 1] = velocityY;
        }
        """

    def pyopenclUpdateParticleVelocities(self):
        num_particles = len(self.particle_canvas.particles)

        positions = np.zeros(2 * num_particles, dtype=np.float32)
        velocities = np.zeros(2 * num_particles, dtype=np.float32)
        colors = np.zeros(num_particles, dtype=np.int32)
        attraction_matrix = np.array(self.particle_canvas.attractionMatrix, dtype=np.float32)

        for i, prtcl in enumerate(self.particle_canvas.particles):
            positions[2 * i] = prtcl.posX
            positions[2 * i + 1] = prtcl.posY
            velocities[2 * i] = prtcl.velX
            velocities[2 * i + 1] = prtcl.velY
            colors[i] = self.particle_canvas.particle_colors.index(prtcl.color)

        positions_buffer = cl.Buffer(self.context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=positions)
        velocities_buffer = cl.Buffer(self.context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=velocities)
        colors_buffer = cl.Buffer(self.context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=colors)
        attraction_matrix_buffer = cl.Buffer(self.context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=attraction_matrix)

        self.program.updateParticleVelocities(self.queue, (num_particles,), None,
                                            positions_buffer, velocities_buffer, colors_buffer,
                                            np.int32(num_particles), np.float32(self.rMax),
                                            np.float32(self.forceFactor), np.float32(self.frictionFactor), np.float32(self.dt),
                                            np.float32(self.particle_canvas.canvas_size['Width']),
                                            np.float32(self.particle_canvas.canvas_size['Height']),
                                            attraction_matrix_buffer)

        cl.enqueue_copy(self.queue, velocities, velocities_buffer)

        for i, prtcl in enumerate(self.particle_canvas.particles):
            prtcl.velX = velocities[2 * i]
            prtcl.velY = velocities[2 * i + 1]
    

    # fuck me im not writing this function myself 
    def force(self, r, a):
        beta = 0.3
        if (r < beta):
            return r / beta - 1
        elif((beta < r) & (r < 1)):
            return a * ( 1 - abs(2 * r - 1 - beta) / (1 - beta))
        else:
            return 0

    def updateParticleVelocities(self):
        for prtcl in self.particle_canvas.particles:
            totalForceX = 0
            totalForceY = 0

            for otherPrtcl in self.particle_canvas.particles:
                if(otherPrtcl == prtcl):
                    continue
                # calculte distance between particles
                rx =  otherPrtcl.posX - prtcl.posX
                ry =  otherPrtcl.posY - prtcl.posY

                # adjust for screen wrapping
                if abs(rx) > self.particle_canvas.canvas_size['Width'] / 2:
                    rx = self.particle_canvas.canvas_size['Width'] - abs(rx)
                if abs(ry) > self.particle_canvas.canvas_size['Height'] / 2:
                    ry = self.particle_canvas.canvas_size['Height'] - abs(ry)
                r = math.sqrt(rx**2 + ry**2)
                # check if distance is greater than 0 and less than rMax
                if ((r > 0) & (r < self.rMax)):
                    f = self.force((r / self.rMax), 
                                   self.particle_canvas.attractionMatrix
                                        [self.particle_canvas.particle_colors.index(otherPrtcl.color)]
                                        [self.particle_canvas.particle_colors.index(prtcl.color)])
                    totalForceX += f * rx / r
                    totalForceY += f * ry / r

            totalForceX *= self.rMax * self.forceFactor
            totalForceY *= self.rMax * self.forceFactor

            prtcl.velX *= self.frictionFactor
            prtcl.velY *= self.frictionFactor

            prtcl.velX += totalForceX * self.dt
            prtcl.velY += totalForceY * self.dt

            self.updateParticlePosition(prtcl)

    def updateParticlePosition(self, prtcl):
        """ Update particle position based on velocity """
        if(self.particle_canvas.canvas_border):
            # revert velocity if particle is out of bounds
            prtcl.posX += prtcl.velX
            if prtcl.posX > self.particle_canvas.canvas_size['Width'] or prtcl.posX < 0:
                prtcl.posX -= prtcl.velX

            prtcl.posY += prtcl.velY
            if prtcl.posY > self.particle_canvas.canvas_size['Height'] or prtcl.posY < 0:
                prtcl.posY -= prtcl.velY
        else:
            # wrap particle around canvas if out of bounds
            prtcl.posX += prtcl.velX
            if prtcl.posX > self.particle_canvas.canvas_size['Width']:
                prtcl.posX = 0
            
            if prtcl.posX < 0:
                prtcl.posX = self.particle_canvas.canvas_size['Width']

            prtcl.posY += prtcl.velY
            if prtcl.posY > self.particle_canvas.canvas_size['Height']:
                prtcl.posY = 0

            if prtcl.posY < 0:
                prtcl.posY = self.particle_canvas.canvas_size['Height']