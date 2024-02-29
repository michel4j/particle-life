import math
import time

import numpy as np
import pyopencl as cl

OLD_OPENCL_KERNEL = """
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

OPENCL_KERNEL = """
// Optimized Kernel code
float force(float r, float a, float beta, float oneMinusBeta) {
    if (r < beta) {
        return r / beta - 1.0f;
    } else if (r < 1.0f) { // Since r is already checked to be greater than beta in the previous condition
        return a * (1.0f - fabs(2.0f * r - 1.0f - beta) * oneMinusBeta);
    } else {
        return 0.0f;
    }
}

__kernel void updateParticleVelocities(__global const float* positions,
                                        __global float* velocities,
                                        __global const int* colors,
                                        const int numParticles,
                                        const float rMax,
                                        const float forceFactor,
                                        const float frictionFactor,
                                        const float dt,
                                        __global const float* attraction_matrix,
                                        const int numColors) {
    int gid = get_global_id(0);

    float totalForceX = 0.0f;
    float totalForceY = 0.0f;

    const float prtclX = positions[2*gid];
    const float prtclY = positions[2*gid + 1];
    const int prtclColorIndex = colors[gid];
    
    const float beta = 0.3f;
    const float oneMinusBeta = 1.0f / (1.0f - beta);

    for (int i = 0; i < numParticles; i++) {
        if (i == gid)
            continue;

        float dx = positions[2*i] - prtclX;
        float dy = positions[2*i + 1] - prtclY;
        float rSquared = dx * dx + dy * dy;
        if (rSquared > 0.0f && rSquared < rMax * rMax) {
            float r = sqrt(rSquared);
            float normalizedR = r / rMax;
            float a = attraction_matrix[prtclColorIndex * numColors + colors[i]]; 
            float f = force(normalizedR, a, beta, oneMinusBeta);
            float factor = f / r;
            totalForceX += factor * dx;
            totalForceY += factor * dy;
        }
    }

    totalForceX *= rMax * forceFactor;
    totalForceY *= rMax * forceFactor;

    // Use temporary variables to store updated velocities to reduce read-modify-write operations
    float newVelocityX = velocities[2*gid] * frictionFactor + totalForceX * dt;
    float newVelocityY = velocities[2*gid + 1] * frictionFactor + totalForceY * dt;

    velocities[2*gid] = newVelocityX;
    velocities[2*gid + 1] = newVelocityY;
}
"""


class Engine:
    def __init__(self, particle_canvas, debug):
        # Inherit particle canvas object
        self.particle_canvas = particle_canvas

        # Time variable
        self.dt = 0.002

        # Particles variables
        self.rMax = 30
        self.frictionHalfLife = 0.02
        self.frictionFactor = math.pow(0.5, self.dt / self.frictionHalfLife)
        self.forceFactor = 0.2

        # Pyopencl 
        self.platform = cl.get_platforms()[0]
        self.device = self.platform.get_devices()[0]
        self.context = cl.Context([self.device])
        self.queue = cl.CommandQueue(self.context)
        self.program = cl.Program(self.context, self.kernel_code()).build()

        # Debug
        self.debug = debug

    def update(self):
        """
        Update particle velocities
        """

        self.update_particles()

        if self.debug:
            begin_ns = time.time_ns()
            move_particles_time_ns = time.time_ns() - begin_ns
            move_particles_time = move_particles_time_ns / 1000000000
            print("1. Move particles:\t\t\t\t" + str(move_particles_time) + " seconds")

    def calculate_friction_factor(self):
        """ Calculate friction factor """
        if self.frictionHalfLife != 0:
            self.frictionFactor = math.pow(0.5, self.dt / self.frictionHalfLife)
        else:
            self.frictionFactor = 0

    def kernel_code(self):
        return OLD_OPENCL_KERNEL

    def update_particles(self):
        """
        Update particle velocities and positions
        """
        num_particles = len(self.particle_canvas.particles)
        num_colors = len(self.particle_canvas.particle_colors)

        positions = np.zeros(2 * num_particles, dtype=np.float32)
        velocities = np.zeros(2 * num_particles, dtype=np.float32)
        colors = np.zeros(num_particles, dtype=np.int32)
        attraction_matrix = np.array(self.particle_canvas.attraction_matrix, dtype=np.float32)

        for i, prtcl in enumerate(self.particle_canvas.particles):
            positions[2 * i] = prtcl.pos_x
            positions[2 * i + 1] = prtcl.pos_y
            velocities[2 * i] = prtcl.vel_x
            velocities[2 * i + 1] = prtcl.vel_y
            colors[i] = self.particle_canvas.particle_colors.index(prtcl.color)

        positions_buffer = cl.Buffer(
            self.context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,
            hostbuf=positions
        )
        velocities_buffer = cl.Buffer(
            self.context, cl.mem_flags.READ_WRITE | cl.mem_flags.COPY_HOST_PTR,
            hostbuf=velocities
        )
        colors_buffer = cl.Buffer(self.context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=colors)
        attraction_matrix_buffer = cl.Buffer(
            self.context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR,
            hostbuf=attraction_matrix
        )

        self.program.updateParticleVelocities(
            self.queue, (num_particles,), None,
            positions_buffer, velocities_buffer, colors_buffer,
            np.int32(num_particles), np.float32(self.rMax),
            np.float32(self.forceFactor), np.float32(self.frictionFactor),
            np.float32(self.dt),
            attraction_matrix_buffer, np.int32(num_colors)
        )

        cl.enqueue_copy(self.queue, velocities, velocities_buffer)

        for i, prtcl in enumerate(self.particle_canvas.particles):
            prtcl.vel_x = velocities[2 * i]
            prtcl.vel_y = velocities[2 * i + 1]
            self.update_particle_position(prtcl)

    def update_particle_position(self, prtcl):
        """ Update particle position based on velocity """
        if self.particle_canvas.canvas_border:
            # revert velocity if particle is out of bounds
            prtcl.pos_x += prtcl.vel_x
            if prtcl.pos_x > self.particle_canvas.canvas_size[
                'Width'] + self.particle_canvas.UI_space or prtcl.pos_x < -1 + self.particle_canvas.UI_space:
                prtcl.pos_x -= prtcl.vel_x

            prtcl.pos_y += prtcl.vel_y
            if prtcl.pos_y > self.particle_canvas.canvas_size['Height'] or prtcl.pos_y < 0:
                prtcl.pos_y -= prtcl.vel_y
        else:
            # wrap particle around canvas if out of bounds
            prtcl.pos_x += prtcl.vel_x
            if prtcl.pos_x > self.particle_canvas.canvas_size['Width'] + self.particle_canvas.UI_space:
                distance_over_border = prtcl.pos_x - self.particle_canvas.canvas_size['Width']
                prtcl.pos_x = distance_over_border

            elif prtcl.pos_x < -1 + self.particle_canvas.UI_space:
                distance_over_border = prtcl.pos_x - self.particle_canvas.UI_space
                prtcl.pos_x = self.particle_canvas.canvas_size[
                                 'Width'] + self.particle_canvas.UI_space + distance_over_border

            prtcl.pos_y += prtcl.vel_y
            if prtcl.pos_y > self.particle_canvas.canvas_size['Height']:
                distance_over_border = prtcl.pos_y - self.particle_canvas.canvas_size['Height']
                prtcl.pos_y = distance_over_border

            elif prtcl.pos_y < -1:
                distance_over_border = prtcl.pos_y
                prtcl.pos_y = self.particle_canvas.canvas_size['Height'] + distance_over_border
