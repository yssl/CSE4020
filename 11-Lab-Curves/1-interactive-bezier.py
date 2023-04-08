from OpenGL.GL import *
from glfw.GLFW import *
import glm
import numpy as np

WINDOW_HEIGHT = 800

g_control_points = [
    glm.vec3(250, 350, 0),
    glm.vec3(350, 450, 0),
    glm.vec3(450, 450, 0),
    glm.vec3(550, 350, 0),
    ]
g_moving_index = None

g_vao_control_points = None
g_vbo_control_points = None
g_vao_curve_points = None
g_vbo_curve_points = None

g_vertex_shader_src = '''
#version 330 core

layout (location = 0) in vec3 vin_pos; 

uniform mat4 MVP;

void main()
{
    gl_Position = MVP * vec4(vin_pos, 1.0);
}
'''

g_fragment_shader_src = '''
#version 330 core

out vec4 FragColor;

uniform vec3 color;

void main()
{
    FragColor = vec4(color, 1.0);
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

def hittest(x, y, control_point):
    if glm.abs(x-control_point.x)<10 and glm.abs(y-control_point.y)<10:
        return True
    else:
        return False

def button_callback(window, button, action, mod):
    global g_control_points, g_moving_index

    if button==GLFW_MOUSE_BUTTON_LEFT:
        x, y = glfwGetCursorPos(window)

        # convert from glfw screen coordinates (relative to the top-left corner)
        # to our camera space coordinates (relative to bottom-left corner) 
        y = WINDOW_HEIGHT - y 

        if action==GLFW_PRESS:
            g_moving_index = None
            for i in range(len(g_control_points)):
                if hittest(x, y, g_control_points[i]):
                    g_moving_index = i
                    break

        elif action==GLFW_RELEASE:
            g_moving_index = None

def cursor_callback(window, xpos, ypos):
    global g_control_points, g_moving_index
    global g_vbo_control_points, g_vbo_curve_points

    ypos = WINDOW_HEIGHT - ypos

    if g_moving_index is not None:

        # update the moving control point position
        g_control_points[g_moving_index].x = xpos
        g_control_points[g_moving_index].y = ypos
        
        # copy updateded control point positions to g_vbo_control_points
        copy_points_data(g_control_points, g_vbo_control_points)

        # copy generated curve point positions from 
        # updated control points to g_vbo_curve_points
        curve_points = generate_curve_points(g_control_points)
        copy_points_data(curve_points, g_vbo_curve_points)

def initialize_vao_for_points(points):
    # create and activate VAO (vertex array object)
    VAO = glGenVertexArrays(1)  # create a vertex array object ID and store it to VAO variable
    glBindVertexArray(VAO)      # activate VAO

    # create and activate VBO (vertex buffer object)
    VBO = glGenBuffers(1)   # create a buffer object ID and store it to VBO variable
    glBindBuffer(GL_ARRAY_BUFFER, VBO)  # activate VBO as a vertex buffer object

    # only allocate VBO and not copy data by specifying the third argument to None
    vertices = glm.array(points)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, None, GL_DYNAMIC_DRAW)

    # configure vertex attributes
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)

    # return VBO along with VAO as it is needed when copying updated point position to VBO
    return VAO, VBO

def copy_points_data(points, vbo):
    glBindBuffer(GL_ARRAY_BUFFER, vbo)  # activate VBO

    # prepare vertex data (in main memory)
    vertices = glm.array(points)

    # only copy vertex data to VBO and not allocating it
    # glBufferSubData(taraget, offset, size, data)
    glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices.ptr)

def generate_curve_points(control_points):
    curve_points = []

    for t in np.linspace(0, 1, 100): # linspace(start, stop, num)
        T = np.array([t**3, t**2, t, 1])

        # Bezier basis matrix
        M = np.array([[-1, 3, -3, 1],
                      [3, -6, 3, 0],
                      [-3, 3, 0, 0],
                      [1, 0, 0, 0]], float)

        P = np.array(control_points)
        p = T @ M @ P

        curve_points.append(glm.vec3(p))

    return curve_points

def main():
    global g_vao_control_points, g_vao_curve_points
    global g_vbo_control_points, g_vbo_curve_points

    # initialize glfw
    if not glfwInit():
        return
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)   # OpenGL 3.3
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)  # Do not allow legacy OpenGl API calls
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE) # for macOS

    # create a window and OpenGL context
    window = glfwCreateWindow(800, WINDOW_HEIGHT, '1-interactive-bezier', None, None)
    if not window:
        glfwTerminate()
        return
    glfwMakeContextCurrent(window)

    # register event callbacks
    glfwSetKeyCallback(window, key_callback);
    glfwSetMouseButtonCallback(window, button_callback)
    glfwSetCursorPosCallback(window, cursor_callback)

    # load shaders & get uniform locations
    shader_program = load_shaders(g_vertex_shader_src, g_fragment_shader_src)
    unif_names = ['color', 'MVP']
    unif_locs = {}
    for name in unif_names:
        unif_locs[name] = glGetUniformLocation(shader_program, name)

    # prepare control points vao & vbo
    g_vao_control_points, g_vbo_control_points = initialize_vao_for_points(g_control_points)
    copy_points_data(g_control_points, g_vbo_control_points)

    # prepare curve points vao & vbo
    curve_points = generate_curve_points(g_control_points)
    g_vao_curve_points, g_vbo_curve_points = initialize_vao_for_points(curve_points)
    copy_points_data(curve_points, g_vbo_curve_points)

    # set point size (for drawing control points)
    glPointSize(20)

    # loop until the user closes the window
    while not glfwWindowShouldClose(window):
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(shader_program)

        # projection matrix & set MVP uniform
        # to make our camera space to have the same size as glfw screen space
        P = glm.ortho(0,800, 0,WINDOW_HEIGHT, -1,1)
        MVP = P
        glUniformMatrix4fv(unif_locs['MVP'], 1, GL_FALSE, glm.value_ptr(MVP))

        # draw control polygon
        glUniform3f(unif_locs['color'], 0, 1, 0)
        glBindVertexArray(g_vao_control_points)
        glDrawArrays(GL_LINE_LOOP, 0, len(g_control_points))
        glDrawArrays(GL_POINTS, 0, len(g_control_points))

        # draw curve
        glUniform3f(unif_locs['color'], 1, 1, 1)
        glBindVertexArray(g_vao_curve_points)
        glDrawArrays(GL_LINE_STRIP, 0, len(curve_points))

        # swap front and back buffers
        glfwSwapBuffers(window)

        # poll events
        glfwPollEvents()

    # terminate glfw
    glfwTerminate()

if __name__ == "__main__":
    main()

