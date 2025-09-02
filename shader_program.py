import glfw
from OpenGL.GL import *
import numpy as np

vertex_shader_source = """
#version 120
attribute vec3 position;
attribute vec3 color;
varying vec3 vColor;
uniform mat4 transform;
void main()
{
    gl_Position = transform * vec4(position, 1.0);
    vColor = color;
}
"""

fragment_shader_source = """
#version 120
varying vec3 vColor;
void main()
{
    gl_FragColor = vec4(vColor, 1.0);
}
"""

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(glGetShaderInfoLog(shader))
    return shader

def create_shader_program(vertex_src, fragment_src):
    vertex_shader = compile_shader(vertex_src, GL_VERTEX_SHADER)
    fragment_shader = compile_shader(fragment_src, GL_FRAGMENT_SHADER)
    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glBindAttribLocation(program, 0, "position")
    glBindAttribLocation(program, 1, "color")
    glLinkProgram(program)
    if glGetProgramiv(program, GL_LINK_STATUS) != GL_TRUE:
        raise RuntimeError(glGetProgramInfoLog(program))
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)
    return program

if not glfw.init():
    raise Exception("Can't initialize GLFW")

window = glfw.create_window(1280, 900, "Modern OpenGL", None, None)
if not window:
    glfw.terminate()
    raise Exception("GLFW window can't be created")

glfw.make_context_current(window)
glClearColor(0.529, 0.808, 0.922, 1.0)

vertices = np.array([
    # positions        # colors
    -0.8, 0.5, 0.0,    1.0, 0.0, 0.0, # Red
     0.8, 0.5, 0.0,    0.0, 1.0, 0.0, # Green
     0.8, -0.5, 0.0,   0.0, 0.0, 1.0, # Blue
    -0.8, -0.5, 0.0,   1.0, 1.0, 0.0, # Yellow
    -0.8, 0.5, 0.0,    1.0, 0.0, 1.0, # Magenta
     0.8, -0.5, 0.0,   0.0, 1.0, 1.0  # Cyan
], dtype=np.float32)

shader_program = create_shader_program(vertex_shader_source, fragment_shader_source)

# Create VBO only (no VAO)
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

import glm  # pip install PyGLM

while not glfw.window_should_close(window):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUseProgram(shader_program)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)

    # Set up position attribute
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * vertices.itemsize, ctypes.c_void_p(0))
    # Set up color attribute
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * vertices.itemsize, ctypes.c_void_p(3 * vertices.itemsize))

    # --- Aspect ratio correction ---
    width, height = glfw.get_framebuffer_size(window)
    aspect = width / height

    # Transformation matrix (move, scale, rotate)
    transform = glm.mat4(1.0)
    transform = glm.scale(transform, glm.vec3(1/aspect, 1.0, 1.0))  # Correct aspect ratio
    transform = glm.translate(transform, glm.vec3(0.2, 0.2, 0.0))
    transform = glm.scale(transform, glm.vec3(0.5, 0.5, 1.0))
    transform = glm.rotate(transform, glm.radians(45), glm.vec3(0, 0, 1))
    loc = glGetUniformLocation(shader_program, "transform")
    glUniformMatrix4fv(loc, 1, GL_FALSE, np.array(transform))

    glDrawArrays(GL_TRIANGLES, 0, 6)

    glDisableVertexAttribArray(0)
    glDisableVertexAttribArray(1)
    glfw.swap_buffers(window)
    glfw.poll_events()

glDeleteBuffers(1, [VBO])
glfw.terminate()
