from OpenGL.GL import *
from glfw.GLFW import *
import glm

def render():
    # glClear(GL_COLOR_BUFFER_BIT)
    # glLoadIdentity()
    # glBegin(GL_TRIANGLES)
    # glVertex2f(0.0, 1.0)
    # glVertex2f(-1.0,-1.0)
    # glVertex2f(1.0,-1.0)
    # glEnd()
    pass

vertexShaderSource = """#version 330 core
layout (location = 0) in vec3 aPos;
void main()
{
   // gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
   gl_Position.xyz = aPos;
   gl_Position.w = 1.0;
}
"""

fragmentShaderSource = """#version 330 core
out vec4 FragColor;
void main()
{
   FragColor = vec4(1.0f, 1.0f, 1.0f, 1.0f);
}
"""

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
    window = glfwCreateWindow(640, 480, '2-first-triangle', None, None)
    if not window:
        glfwTerminate()
        return

    glfwMakeContextCurrent(window)

    # build and compile our shader program
    # ------------------------------------
    # vertex shader
    vertexShader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertexShader, vertexShaderSource)
    glCompileShader(vertexShader)
    
    # check for shader compile errors
    success = glGetShaderiv(vertexShader, GL_COMPILE_STATUS)
    if (not success):
        infoLog = glGetShaderInfoLog(vertexShader)
        print("ERROR::SHADER::VERTEX::COMPILATION_FAILED\n" + infoLog.decode())
        
    # fragment shader
    fragmentShader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragmentShader, fragmentShaderSource)
    glCompileShader(fragmentShader)
    
    # check for shader compile errors
    success = glGetShaderiv(fragmentShader, GL_COMPILE_STATUS)
    if (not success):
        infoLog = glGetShaderInfoLog(fragmentShader)
        print("ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n" + infoLog.decode())
    # link shaders
    shaderProgram = glCreateProgram()
    glAttachShader(shaderProgram, vertexShader)
    glAttachShader(shaderProgram, fragmentShader)
    glLinkProgram(shaderProgram)
    # check for linking errors
    success = glGetProgramiv(shaderProgram, GL_LINK_STATUS)
    if (not success):
        infoLog = glGetProgramInfoLog(shaderProgram)
        print("ERROR::SHADER::PROGRAM::LINKING_FAILED\n" + infoLog.decode())
        
    glDeleteShader(vertexShader)
    glDeleteShader(fragmentShader)

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
