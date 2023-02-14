from OpenGL.GL import *
from glfw.GLFW import *
import glm

g_vertex_shader_src = '''
#version 330 core
layout (location = 0) in vec3 aPos;
void main()
{
   // gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
   gl_Position.xyz = aPos;
   gl_Position.w = 1.0;
}
'''

g_fragment_shader_src = '''
#version 330 core
out vec4 FragColor;
void main()
{
   FragColor = vec4(1.0f, 1.0f, 1.0f, 1.0f);
}
'''

def load_shaders(vertex_shader_source, fragment_shader_source):
    # build and compile our shader program
    # ------------------------------------
    # vertex shader
    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, vertex_shader_source)
    glCompileShader(vertex_shader)
    
    # check for shader compile errors
    success = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)
    if (not success):
        infoLog = glGetShaderInfoLog(vertex_shader)
        print("ERROR::SHADER::VERTEX::COMPILATION_FAILED\n" + infoLog.decode())
        
    # fragment shader
    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, fragment_shader_source)
    glCompileShader(fragment_shader)
    
    # check for shader compile errors
    success = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS)
    if (not success):
        infoLog = glGetShaderInfoLog(fragment_shader)
        print("ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n" + infoLog.decode())

    # link shaders
    shaderProgram = glCreateProgram()
    glAttachShader(shaderProgram, vertex_shader)
    glAttachShader(shaderProgram, fragment_shader)
    glLinkProgram(shaderProgram)

    # check for linking errors
    success = glGetProgramiv(shaderProgram, GL_LINK_STATUS)
    if (not success):
        infoLog = glGetProgramInfoLog(shaderProgram)
        print("ERROR::SHADER::PROGRAM::LINKING_FAILED\n" + infoLog.decode())
        
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return shaderProgram


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
    window = glfwCreateWindow(800, 600, '2-first-triangle', None, None)
    if not window:
        glfwTerminate()
        return

    glfwMakeContextCurrent(window)

    # load shaders
    shaderProgram = load_shaders(g_vertex_shader_src, g_fragment_shader_src)

    # register key callback for escape key
    glfwSetKeyCallback(window, key_callback);

    # create and bind VAO (vertex array object)
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vertices = glm.array(glm.float32,
        -1.0, -1.0, 0.0, # left  
         1.0, -1.0, 0.0, # right 
         0.0,  1.0, 0.0  # top
    )

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices.ptr, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * glm.sizeof(glm.float32), None)
    glEnableVertexAttribArray(0)

    # loop until the user closes the window
    while not glfwWindowShouldClose(window):
        # update

        # render
        # glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(shaderProgram)
        glBindVertexArray(vao)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        # swap front and back buffers
        glfwSwapBuffers(window)

        # poll events
        glfwPollEvents()

    # terminate glfw
    glfwTerminate()

if __name__ == "__main__":
    main()
