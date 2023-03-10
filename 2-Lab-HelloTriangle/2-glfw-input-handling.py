from OpenGL.GL import *
from glfw.GLFW import *

def key_callback(window, key, scancode, action, mods):
    if key==GLFW_KEY_ESCAPE and action==GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE);
    elif key==GLFW_KEY_A:
        if action==GLFW_PRESS:
            print('press a')
        elif action==GLFW_RELEASE:
            print('release a')
        elif action==GLFW_REPEAT:
            print('repeat a')
    elif key==GLFW_KEY_SPACE and action==GLFW_PRESS:
        print ('press space: (%d, %d)'%glfwGetCursorPos(window))

def cursor_callback(window, xpos, ypos):
    print('mouse cursor moving: (%d, %d)'%(xpos, ypos))

def button_callback(window, button, action, mod):
    if button==GLFW_MOUSE_BUTTON_LEFT:
        if action==GLFW_PRESS:
            print('press left btn: (%d, %d)'%glfwGetCursorPos(window))
        elif action==GLFW_RELEASE:
            print('release left btn: (%d, %d)'%glfwGetCursorPos(window))
     
def scroll_callback(window, xoffset, yoffset):
    print('mouse wheel scroll: %d, %d'%(xoffset, yoffset))

def main():
    # initialize glfw
    if not glfwInit():
        return
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)   # OpenGL 3.3
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)  # Do not allow legacy OpenGl API calls
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE) # for macOS

    # create a window and OpenGL context
    window = glfwCreateWindow(800, 800, '2-glfw-input-handling', None, None)
    if not window:
        glfwTerminate()
        return
    glfwMakeContextCurrent(window)

    # register event callbacks
    glfwSetKeyCallback(window, key_callback);
    glfwSetCursorPosCallback(window, cursor_callback)
    glfwSetMouseButtonCallback(window, button_callback)
    glfwSetScrollCallback(window, scroll_callback)

    # loop until the user closes the window
    while not glfwWindowShouldClose(window):
        # render

        # swap front and back buffers
        glfwSwapBuffers(window)

        # poll events
        glfwPollEvents()

    # terminate glfw
    glfwTerminate()

if __name__ == "__main__":
    main()
