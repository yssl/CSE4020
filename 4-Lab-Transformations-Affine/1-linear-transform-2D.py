from OpenGL.GL import *
from glfw.GLFW import *
import glm
import ctypes
import numpy as np

g_vertex_shader_src = '''
#version 330 core

layout (location = 0) in vec3 vin_pos; 
layout (location = 1) in vec3 vin_color; 

out vec4 vout_color;

uniform mat2 M;

void main()
{
    gl_Position = vec4(0, 0, 0, 1.0);
    gl_Position.xy = M * vin_pos.xy;
    vout_color = vec4(vin_color, 1);
}
'''

g_fragment_shader_src = '''
#version 330 core

in vec4 vout_color;

out vec4 FragColor;

void main()
{
    FragColor = vout_color;
}
'''

def load_shaders(vertex_shader_source, fragment_shader_source):
    # build and compile our shader program
    # ------------------------------------
    
    # vertex shader 
    vertex_shader = glCreateShader(GL_VERTEX_SHADER)    # create an empty shader object
    glShaderSource(vertex_shader, vertex_shader_source) # provide shader source code
    glCompileShader(vertex_shader)                      # compile the shader object
    
    # check for shader compile errors
    success = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)
    if (not success):
        infoLog = glGetShaderInfoLog(vertex_shader)
        print("ERROR::SHADER::VERTEX::COMPILATION_FAILED\n" + infoLog.decode())
        
    # fragment shader
    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)    # create an empty shader object
    glShaderSource(fragment_shader, fragment_shader_source) # provide shader source code
    glCompileShader(fragment_shader)                        # compile the shader object
    
    # check for shader compile errors
    success = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS)
    if (not success):
        infoLog = glGetShaderInfoLog(fragment_shader)
        print("ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n" + infoLog.decode())

    # link shaders
    shader_program = glCreateProgram()               # create an empty program object
    glAttachShader(shader_program, vertex_shader)    # attach the shader objects to the program object
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)                    # link the program object

    # check for linking errors
    success = glGetProgramiv(shader_program, GL_LINK_STATUS)
    if (not success):
        infoLog = glGetProgramInfoLog(shader_program)
        print("ERROR::SHADER::PROGRAM::LINKING_FAILED\n" + infoLog.decode())
        
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return shader_program    # return the shader program


def key_callback(window, key, scancode, action, mods):
    if key==GLFW_KEY_ESCAPE and action==GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE);

def main():
    # initialize glfw
    if not glfwInit():
        return
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)   # OpenGL 3.3
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)  # Do not allow legacy OpenGl API calls
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE) # for macOS

    # create a window and OpenGL context
    window = glfwCreateWindow(800, 800, '1', None, None)
    if not window:
        glfwTerminate()
        return
    glfwMakeContextCurrent(window)

    # register event callbacks
    glfwSetKeyCallback(window, key_callback);

    # load shaders
    shader_program = load_shaders(g_vertex_shader_src, g_fragment_shader_src)

    # get uniform locations
    M_loc = glGetUniformLocation(shader_program, 'M')
    
    # update uniforms 
    glUseProgram(shader_program)    # updating uniform require you to first activate the shader program 

    use_numpy = True
    # use_numpy = False

    if(use_numpy):
        # numpy

        # 2x2 identity matrix 
        # M = np.array([[1., 0.],
                      # [0., 1.]])   # or
        M = np.identity(2)

        # # uniform scaling
        # M = np.array([[2., 0.],
                      # [0., 2.]])

        # # nonuniform scaling
        # M = np.array([[2., 0.],
                      # [0., 1.]])

        # # reflection
        # M = np.array([[-1., 0],
                      # [0., 1.]])

        # # shearing in x
        # M = np.array([[1., 2.],
                      # [0., 1.]])

        # # rotation
        # th = np.radians(30)
        # M = np.array([[np.cos(th), -np.sin(th)],
                      # [np.sin(th),  np.cos(th)]])

        # print(M)

        # note that 'transpose' (3rd parameter) is set to GL_TRUE
        # because numpy array is row-major.
        glUniformMatrix2fv(M_loc, 1, GL_TRUE, M)
    else:
        # glm

        # 2x2 identity matrix 
        # M = glm.mat2(1., 0.,
                     # 0., 1.)
        M = glm.mat2() 

        # # uniform scaling
        # M = glm.mat2(2., 0.,
                     # 0., 2.)

        # # nonuniform scaling
        # M = glm.mat2(2., 0.,
                     # 0., 1.)

        # # reflection
        # M = glm.mat2(-1., 0.,
                     # 0., 1.)

        # # shearing in x
        # # # not this matrix!:
        # # M = glm.mat2(1., 2.,
                     # # 0., 1.)
        # # note that glm matrix is column-major (numpy array is row-major)
        # # correct matrix is:
        # M = glm.mat2(1., 0.,
                     # 2., 1.)

        # # rotation
        # th = np.radians(30)
        # M = glm.mat2(np.cos(th), np.sin(th),
                    # -np.sin(th), np.cos(th))

        # print(M)

        # note that 'transpose' (3rd parameter) is set to GL_FALSE
        # because glm matrix is column-major.
        glUniformMatrix2fv(M_loc, 1, GL_FALSE, glm.value_ptr(M))

    # prepare vertex data (in main memory)
    vertices = glm.array(glm.float32,
        # position        # color
         0.0, 0.0, 0.0,  1.0, 0.0, 0.0, # v0
         0.5, 0.0, 0.0,  0.0, 1.0, 0.0, # v1
         0.0, 0.5, 0.0,  0.0, 0.0, 1.0, # v2
    )

    # create and activate VAO (vertex array object)
    VAO = glGenVertexArrays(1)  # create a vertex array object ID and store it to VAO variable
    glBindVertexArray(VAO)      # activate VAO

    # create and activate VBO (vertex buffer object)
    VBO = glGenBuffers(1)   # create a buffer object ID and store it to VBO variable
    glBindBuffer(GL_ARRAY_BUFFER, VBO)  # activate VBO as a vertex buffer object

    # copy vertex data to VBO
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW) # allocate GPU memory for and copy vertex data to the currently bound vertex buffer

    # configure vertex positions
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)

    # configure vertex colors
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * glm.sizeof(glm.float32), ctypes.c_void_p(3*glm.sizeof(glm.float32)))
    glEnableVertexAttribArray(1)

    # loop until the user closes the window
    while not glfwWindowShouldClose(window):
        # update

        # render
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(shader_program)

        glBindVertexArray(VAO)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        # swap front and back buffers
        glfwSwapBuffers(window)

        # poll events
        glfwPollEvents()

    # terminate glfw
    glfwTerminate()

if __name__ == "__main__":
    main()
