import math
import time
import pyopencl as cl
import numpy as np

class Engine():
    def __init__(self, particle_canvas, debug):
        # Inherit particle canvas object
        self.particle_canvas = particle_canvas
        
        # Time varialbe
        self.dt = 0.005

        # Particles variables
        self.rMax = 30
        self.frictionHalfLife = 0.04
        self.frictionFactor = math.pow(0.5, self.dt / self.frictionHalfLife)
        self.forceFactor = 0.5

        # Pyopencl 
        self.platform = cl.get_platforms()[0]
        self.device = self.platform.get_devices()[0]
        self.context = cl.Context([self.device])
        self.queue = cl.CommandQueue(self.context)
        self.program = cl.Program(self.context, self.kernelCode()).build()

        # Debug
        self.debug = debug


        

    def update(self):
        """ Update particle velocities """
        if(self.debug):
            begin = time.time_ns()  / (10 ** 9)
        
        self.updateParticles()

        if(self.debug):
            print("1. Move particles:\t\t\t\t" + str(time.time_ns()  / (10 ** 9) - begin) + " seconds")

    def calculateFrictionFactor(self):
        """ Calculate friction factor """
        if self.frictionHalfLife != 0:
            self.frictionFactor = math.pow(0.5, self.dt / self.frictionHalfLife)
        else:
            self.frictionFactor = 0

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
                                            __global float* attraction_matrix,
                                            int numColors) {
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
                float r = sqrt(rx * rx + ry * ry);

                // Check if distance is greater than 0 and less than rMax
                if (r > 0 && r < rMax) {
                    float a = attraction_matrix[prtclColorIndex * numColors + otherPrtclColorIndex]; 
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

    def updateParticles(self):
        """ Update particle velocities and positions"""	
        num_particles = len(self.particle_canvas.particles)
        num_colors = len(self.particle_canvas.particle_colors)

        positions = np.zeros(2 * num_particles, dtype=np.float32)
        velocities = np.zeros(2 * num_particles, dtype=np.float32)
        colors = np.zeros(num_particles, dtype=np.int32)
        attraction_matrix = np.array(self.particle_canvas.attraction_matrix, dtype=np.float32)

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
                                            attraction_matrix_buffer, np.int32(num_colors))

        cl.enqueue_copy(self.queue, velocities, velocities_buffer)

        for i, prtcl in enumerate(self.particle_canvas.particles):
            prtcl.velX = velocities[2 * i]
            prtcl.velY = velocities[2 * i + 1]
            self.updateParticlePosition(prtcl)

    def updateParticlePosition(self, prtcl):
        """ Update particle position based on velocity """
        if(self.particle_canvas.canvas_border):
            # revert velocity if particle is out of bounds
            prtcl.posX += prtcl.velX
            if prtcl.posX > self.particle_canvas.canvas_size['Width'] + self.particle_canvas.UI_space or prtcl.posX < -1 + self.particle_canvas.UI_space:
                prtcl.posX -= prtcl.velX

            prtcl.posY += prtcl.velY
            if prtcl.posY > self.particle_canvas.canvas_size['Height'] or prtcl.posY < 0:
                prtcl.posY -= prtcl.velY
        else:
            # wrap particle around canvas if out of bounds
            prtcl.posX += prtcl.velX
            if prtcl.posX > self.particle_canvas.canvas_size['Width'] + self.particle_canvas.UI_space:
                distance_over_border = prtcl.posX - self.particle_canvas.canvas_size['Width']
                prtcl.posX = distance_over_border
            
            elif prtcl.posX < -1 + self.particle_canvas.UI_space:
                distance_over_border = prtcl.posX - self.particle_canvas.UI_space
                prtcl.posX = self.particle_canvas.canvas_size['Width'] + self.particle_canvas.UI_space + distance_over_border

            prtcl.posY += prtcl.velY
            if prtcl.posY > self.particle_canvas.canvas_size['Height']:
                distance_over_border = prtcl.posY - self.particle_canvas.canvas_size['Height']
                prtcl.posY = distance_over_border

            elif prtcl.posY < -1:
                distance_over_border = prtcl.posY
                prtcl.posY = self.particle_canvas.canvas_size['Height'] + distance_over_border
            