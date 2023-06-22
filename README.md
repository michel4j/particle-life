# Particle-Life
Python based simulation of Particle Life that uses OpenCL and OpenGL.  

# How to run the program
This application uses Pyopencl to calculate forces between particles, thus OpenCL needs to be installed on your system.
Rendering the particles is done OpenGL, and older version (2.0) is used for this.   

# Dependencies
* numpy (1.24.3)  
  pip install numpy  
  
* pynput (1.7.6)  
  pip install pynput
  
*pyopencl (2023.1)
  pip install pyopencl

*pyglet (1.5.27 - an older maintenance version)
  git clone https://github.com/pyglet/pyglet.git
  cd pyglet
  git checkout pyglet-1.5-maintenance
  python setup.py install --user
