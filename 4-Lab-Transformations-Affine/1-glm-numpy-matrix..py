# todo

# 2-lab, 2-assign, 2-quiz, 3-lab, 3-quiz 이미지 비율 및 윈도우 크기 변경

# 2-Lab pptx:
# 7 page - We'll use Python binding for OpenGL, PyOpenGL.
# 12 page -  We'll use Python binding for GLFW, glfw

# before 19 page - add numpy page
# NumPy is a general-purpose numerical computing library for Python
# that provides high-performance array operations (matrix & vector operations) 
# and linear algebra functions. 
# It is widely used in scientific computing, data analysis, and machine learning, and it also has some support for OpenGL-related operations.

# 19 page - PyGLM is a Python extension based on GLM.
# PyGLM is specifically designed to work well
# if you are developing computer graphics applications with PyOpenGL, PyGLM might be a better choice because it provides a more comprehensive set of functions and data types that are specifically designed for this purpose. However, if you need to perform general numerical computations, including linear algebra, NumPy might be a better choice due to its versatility and performance.

# Both PyGLM and NumPy are powerful math libraries that can be used for PyOpenGL development, but they have different strengths and weaknesses.

# PyGLM is a Python extension for OpenGL Mathematics (GLM), a C++ library designed for computer graphics programming. It provides a comprehensive set of functions and data types for vector and matrix operations, quaternion calculations, and geometric algorithms, which makes it an excellent choice for PyOpenGL development. PyGLM is specifically designed to work well with PyOpenGL and provides easy integration with other popular Python libraries, such as NumPy.

# NumPy, on the other hand, is a general-purpose numerical computing library for Python that provides high-performance array operations and linear algebra functions. It is widely used in scientific computing, data analysis, and machine learning, and it also has some support for OpenGL-related operations. NumPy provides a flexible and easy-to-use interface for array manipulation and broadcasting, making it an excellent choice for implementing algorithms that involve large arrays of data.

# In general, if you are developing computer graphics applications with PyOpenGL, PyGLM might be a better choice because it provides a more comprehensive set of functions and data types that are specifically designed for this purpose. However, if you need to perform general numerical computations, including linear algebra, NumPy might be a better choice due to its versatility and performance.


import glm
import numpy as np

# 
M_np = np.array([[1., 2.],
                 [0., 1.]])
print('M_np:')
print(M_np)
print()

# numpy indexing: [row_index, col_index]
print('M_np[0,1]:', M_np[0,1])
print()

#
M_glm = glm.mat2(1., 0.,
                 2., 1.)
print('M_glm:')
print(M_glm)
print()

# glm indexing: [col_index, row_index]
print('M_glm[0,1]:', M_glm[0,1])


# NumPy and GLM use different conventions for storing multi-dimensional arrays, which can affect how data is accessed and manipulated in certain operations.

# NumPy uses a row-major storage convention, where the elements of a multi-dimensional array are stored in contiguous memory locations row by row. This means that the elements of the first row of a 2D array are stored consecutively in memory, followed by the elements of the second row, and so on. This convention is sometimes called "C-style" or "row-major" ordering.

# On the other hand, GLM uses a column-major storage convention, where the elements of a multi-dimensional array are stored in contiguous memory locations column by column. This means that the elements of the first column of a 2D array are stored consecutively in memory, followed by the elements of the second column, and so on. This convention is sometimes called "Fortran-style" or "column-major" ordering.

# The difference in storage conventions can lead to some confusion when using both libraries together, especially when passing arrays between them. In general, it is important to make sure that the data is properly transposed or reshaped to match the expected storage convention of each library.

# Fortunately, both NumPy and GLM provide functions for converting between different storage conventions. In NumPy, the numpy.ndarray.T attribute can be used to transpose an array, while in GLM, the glm.transpose function can be used to transpose a matrix. Additionally, both libraries support the use of custom strides and memory layouts to control the storage order of arrays.


