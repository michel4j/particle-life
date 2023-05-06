import math
import enum
import random

# Canvas
canvasSizeXMin = 0
canvasSizeXMax = 800
canvasSizeYMin = 0
canvasSizeYMax = 800
border = False

# Time
dt = 0.01

# Particles 
rMax = 150
particles = []
frictionHalfLife = 0.04
frictionFactor = math.pow(0.5, dt / frictionHalfLife)

class Color(enum.Enum):
   red = 0
   blue = 1
   green = 2

# Attraction matrices
matrix1 =[[1,    0.8,  0.6,  0.4    ], 
          [0.8,  1,    0.8,  0.6    ],
          [0.6,  0.8,  1,    0.8    ],
          [0.4,  0.6,  0.8,  1      ]]

matrix2 =[[0.3,   -0.5,   -0.3, 0.3  ], 
          [1,     0.5,    1,    0.5  ],
          [-0.5,  1,      0.5,  -1   ],
          [-0.3,  1,      0.5,  0.8  ]]

matrix3 =[[-1,    0.8,  0.6,  0.4    ], 
          [0.8,  -1,    0.8,  0.6    ],
          [0.6,  0.8,  -1,    0.8    ],
          [0.4,  0.6,  0.8,  -1      ]]

matrix3 =[[-1,    0.8,  0.6,  0.4    ], 
          [0.8,  -1,    -0.8,  0.6    ],
          [-0.6,  0.8,  -1,    0.8    ],
          [0.4,  -0.6,  0.8,  -1      ]]

def generateRandomAttractionMatrix():
    matrix = [[0 for x in range(len(Color)+1)] for y in range(len(Color)+1)]
    for i in range(len(Color)+1):
        for j in range(len(Color)+1):
            matrix[i][j] = random.uniform(-1, 1)
    return matrix

#matrix = generateRandomAttractionMatrix()
matrix = matrix3