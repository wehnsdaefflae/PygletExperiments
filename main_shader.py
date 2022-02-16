import pyglet
from pyglet import gl
import ctypes


class Triangle:
  def __init__(self):
    self.triangle = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
                      0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
                      0.0,  0.5, 0.0, 0.0, 0.0, 1.0]

    with open("shader_code/triangle.frag", mode="br") as f:
      self.fragment_shader = f.read()

    with open("shader_code/triangle.vert", mode="br") as f:
      self.vertex_shader = f.read()

    vertex_buff = ctypes.create_string_buffer(self.vertex_shader)
    c_vertex = ctypes.cast(ctypes.pointer(ctypes.pointer(vertex_buff)), ctypes.POINTER(ctypes.POINTER(gl.GLchar)))
    vertex_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
    gl.glShaderSource(vertex_shader, 1, c_vertex, None)
    gl.glCompileShader(vertex_shader)

    fragment_buff = ctypes.create_string_buffer(self.fragment_shader)
    c_fragment = ctypes.cast(ctypes.pointer(ctypes.pointer(fragment_buff)), ctypes.POINTER(ctypes.POINTER(gl.GLchar)))
    fragment_shader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
    gl.glShaderSource(fragment_shader, 1, c_fragment, None)
    gl.glCompileShader(fragment_shader)

    shader = gl.glCreateProgram()
    gl.glAttachShader(shader, vertex_shader)
    gl.glAttachShader(shader, fragment_shader)
    gl.glLinkProgram(shader)

    gl.glUseProgram(shader)

    vbo = gl.GLuint(0)
    gl.glGenBuffers(1, vbo)

    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, 72, (gl.GLfloat * len(self.triangle))(*self.triangle), gl.GL_STATIC_DRAW)

    #positions
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 24, ctypes.c_void_p(0))
    gl.glEnableVertexAttribArray(0)

    #colors
    gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 24, ctypes.c_void_p(12))
    gl.glEnableVertexAttribArray(1)


class Canvas(pyglet.window.Window):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.set_minimum_size(400, 300)
    gl.glClearColor(0.2, 0.3, 0.2, 1.0)

    self.triangle = Triangle()

  def on_draw(self):
    self.clear()
    gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)

  def on_resize(self, width, height):
    gl.glViewport(0, 0, width, height)

  def run(self):
    pyglet.app.run()

if __name__ == "__main__":
  window = Canvas(1280, 720, "tutorial", resizable=True)
  window.run()
