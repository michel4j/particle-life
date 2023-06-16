import math
import time
import pyopencl as cl
import numpy as np



class Engine():
    def __init__(self, particle_canvas, debug = False):
        # Time
        self.dt = 0.02

        # Particles 
        self.rMax = 180
        self.frictionHalfLife = 0.04
        self.frictionFactor = math.pow(0.5, self.dt / self.frictionHalfLife)
        self.forceFactor = 0.5
        
        # Canvas
        self.particleCanvas = particle_canvas

        # Pyopencl 
        self.platform = cl.get_platforms()[0]
        self.device = self.platform.get_devices()[0]
        self.context = cl.Context([self.device])
        self.queue = cl.CommandQueue(self.context)

        self.program = cl.Program(self.context, self.kernelCode()).build()

        self.debug = debug

    def update(self):
        """ Update particle velocities """
        if(self.debug):
            begin = time.time_ns()  / (10 ** 9)
        
        self.pyopenclUpdateParticleVelocities()

        if(self.debug):
            print("1. Calculate forces between particles:\t\t" + str(time.time_ns()  / (10 ** 9) - begin) + " seconds")

    def kernelCode(self):
        return"""
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
                                            int num_particles,
                                            float r_max,
                                            float force_factor,
                                            float friction_factor,
                                            float dt) {
            int gid = get_global_id(0);

            float totalForceX = 0;
            float totalForceY = 0;

            for (int i = 0; i < num_particles; i++) {
                if (i == gid)
                    continue;

                float rx = positions[2 * i] - positions[2 * gid];
                float ry = positions[2 * i + 1] - positions[2 * gid];

                // adjust for screen wrapping
                if (fabs(rx) > r_max / 2)
                    rx = r_max - fabs(rx);
                if (fabs(ry) > r_max / 2)
                    ry = r_max - fabs(ry);

                float r = sqrt(rx * rx + ry * ry);

                if (r > 0 && r < r_max) {
                    float f = force(r / r_max, 1.0);  // You can replace '1.0' with the appropriate value
                    totalForceX += f * rx / r;
                    totalForceY += f * ry / r;
                }
            }

            totalForceX *= r_max * force_factor;
            totalForceY *= r_max * force_factor;

            velocities[2 * gid] *= friction_factor;
            velocities[2 * gid + 1] *= friction_factor;

            velocities[2 * gid] += totalForceX * dt;
            velocities[2 * gid + 1] += totalForceY * dt;
        }
        """

    def pyopenclUpdateParticleVelocities(self):
        num_particles = len(self.particleCanvas.particles)

        positions = np.zeros(2 * num_particles, dtype=np.float32)
        velocities = np.zeros(2 * num_particles, dtype=np.float32)

        for i, prtcl in enumerate(self.particleCanvas.particles):
            positions[2 * i] = prtcl.posX
            positions[2 * i + 1] = prtcl.posY
            velocities[2 * i] = prtcl.velX
            velocities[2 * i + 1] = prtcl.velY

        positions_buffer = cl.Buffer(self.context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=positions)
        velocities_buffer = cl.Buffer(self.context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR, hostbuf=velocities)

        self.program.updateParticleVelocities(self.queue, (num_particles,), None,
                                        positions_buffer, velocities_buffer,
                                        np.int32(num_particles), np.float32(self.rMax),
                                        np.float32(self.forceFactor), np.float32(self.frictionFactor),
                                        np.float32(self.dt))

        cl.enqueue_copy(self.queue, velocities, velocities_buffer)

        for i, prtcl in enumerate(self.particleCanvas.particles):
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
        for prtcl in self.particleCanvas.particles:
            totalForceX = 0
            totalForceY = 0

            for otherPrtcl in self.particleCanvas.particles:
                if(otherPrtcl == prtcl):
                    continue
                # calculte distance between particles
                rx =  otherPrtcl.posX - prtcl.posX
                ry =  otherPrtcl.posY - prtcl.posY

                # adjust for screen wrapping
                if abs(rx) > self.particleCanvas.canvas_size['Width'] / 2:
                    rx = self.particleCanvas.canvas_size['Width'] - abs(rx)
                if abs(ry) > self.particleCanvas.canvas_size['Height'] / 2:
                    ry = self.particleCanvas.canvas_size['Height'] - abs(ry)
                r = math.sqrt(rx**2 + ry**2)
                # check if distance is greater than 0 and less than rMax
                if ((r > 0) & (r < self.rMax)):
                    f = self.force((r / self.rMax), 
                                   self.particleCanvas.attractionMatrix
                                        [self.particleCanvas.particle_colors.index(otherPrtcl.color)]
                                        [self.particleCanvas.particle_colors.index(prtcl.color)])
                    totalForceX += f * rx / r
                    totalForceY += f * ry / r

            totalForceX *= self.rMax * self.forceFactor
            totalForceY *= self.rMax * self.forceFactor

            prtcl.velX *= self.frictionFactor
            prtcl.velY *= self.frictionFactor

            prtcl.velX += totalForceX * self.dt
            prtcl.velY += totalForceY * self.dt