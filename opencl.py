import numpy as np
import pyopencl as cl
import time

getal_1_np = 50
getal_2_np = 100

ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)

mf = cl.mem_flags

prg = cl.Program(ctx, """
__kernel void sum(int getal_1_g, int getal_2_g, __global int *res_g)
{
  int gid = get_global_id(0);
  res_g[gid] = getal_1_g + getal_2_g;
}
""").build()

res = np.empty(1, dtype=np.int32)
res_g = cl.Buffer(ctx, mf.WRITE_ONLY, res.nbytes)
knl = prg.sum  # Use this Kernel object for repeated calls

begin = time.time()  # Start time
knl(queue, res.shape, None, np.int32(getal_1_np), np.int32(getal_2_np), res_g)

res_np = np.empty_like(getal_1_np)
cl.enqueue_copy(queue, res_np, res_g)

total_time = time.time() - begin  # End time

# Check on CPU with Numpy:
print("Result:" + str(res_np))
print("Total time: " + str(total_time))
assert np.allclose(res_np, getal_1_np + getal_2_np)