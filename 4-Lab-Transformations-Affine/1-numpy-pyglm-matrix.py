import glm
import numpy as np

# numpy matrix creation
M_np = np.array([[1., 2.],
                 [0., 1.]])
print('M_np:')
print(M_np)
print()

# M_np:
# [[1. 2.]
#  [0. 1.]]

# numpy indexing: [row_index, col_index]

# first row
print('M_np[0]:', M_np[0])

# element at first row, second col
print('M_np[0,1]:', M_np[0,1])

# M_np[0]: [1. 2.]
# M_np[0,1]: 2.0

print()

# glm matrix creation
M_glm = glm.mat2(1., 0.,
                 2., 1.)
print('M_glm:')
print(M_glm)
print()

# M_glm:
# [            1 ][            2 ]
# [            0 ][            1 ]

# glm indexing: [col_index, row_index]

# first col
print('M_glm[0]:', M_glm[0])

# element at second row, first col
print('M_glm[0,1]:', M_glm[0,1])

# M_glm[0]: mvec2( 1, 0 )
# M_glm[0,1]: 0.0
