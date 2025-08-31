import glfw 
from OpenGL.GL import *
import numpy as np 


if not glfw.init():
    raise Exception("Can't initialize GLFW")

# monitor = glfw.get_primary_monitor()
window = glfw.create_window(1280, 900, "Learning OpenGL", None, None)

if not window:
    glfw.terminate()
    raise Exception("GLFW window can't be created")

glfw.make_context_current(window)
glClearColor(0.529, 0.808, 0.922, 1.0)

vertices = np.array([
    -0.8, 0.5, 0.0,
    0.8, 0.5, 0.0,
    0.8, -0.5, 0.0,
    -0.8, -0.5, 0.0,
    -0.8, 0.5, 0.0,
    0.8, -0.5, 0.0
    ], dtype=np.float32)

colors = np.array([
    1.0, 0.0, 0.0, # Red
    0.0, 1.0, 0.0, # Green
    0.0, 0.0, 1.0, # Blue
    1.0, 1.0, 0.0, # Yellow
    1.0, 0.0, 1.0, # Magenta
    0.0, 1.0, 1.0 # Cyan
], dtype=np.float32)

while not glfw.window_should_close(window):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glTranslatef(0.2, 0.2, 0.0)
    glScalef(0.5, 0.5, 1.0)
    glRotatef(45, 0, 0, 1)

    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    
    glVertexPointer(3, GL_FLOAT, 0, vertices)
    glColorPointer(3, GL_FLOAT, 0, colors)
    glDrawArrays(GL_TRIANGLES, 0, 6)

    glDisableClientState(GL_COLOR_ARRAY)
    glDisableClientState(GL_VERTEX_ARRAY)
    glfw.swap_buffers(window)
    glfw.poll_events()