import glfw
import OpenGL.GL as gl
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from math import sin, cos


class openGlWindow:

    def __init__(self, width: int, height: int, title: str):

        if not glfw.init():
            raise Exception("Glfw cannot be initialized!!")

        self._window = glfw.create_window(width, height, title, None, None)

        if not self._window:
            glfw.terminate()
            raise Exception("Glfw window cannot be created!!")

        glfw.set_window_pos(self._window, 400, 200)

        glfw.make_context_current(self._window)

        self.triangle = triangle(vector3(-0.5, -0.5), vector3(0.5, -0.5), vector3(0.0, 0.5))
        self.triangle.compile_shaders()
        self.triangle.draw()

        # self.triangle = deptriangle(vector3(-0.5, -0.5), vector3(0.5, -0.5), vector3(0.0, 0.5))

        self.set_gl_settings()

    @staticmethod
    def set_gl_settings():
        gl.glClearColor(0, 0.1, 0.1, 1)
        # self.triangle.set_gl_settings()

    def start(self):
        while not glfw.window_should_close(self._window):
            glfw.poll_events()

            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            ct = glfw.get_time()

            # self.triangle.draw()
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)

            glfw.swap_buffers(self._window)

        glfw.terminate()


class vector3:

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z

    def tolist(self):
        return [self.x, self.y, self.z]


class triangle:

    def __init__(self, posx: vector3, posy: vector3, posz: vector3):
        self._buffer = [posx.x, posx.y, posx.z,
                        posy.x, posy.y, posy.z,
                        posz.x, posz.y, posz.z,
                        1.0, 0.0, 0.0,
                        0.0, 1.0, 0.0,
                        0.0, 0.0, 1.0]

        self._buffer = np.array(self._buffer, dtype=np.float32)
        self._shader = None

    def compile_shaders(self):
        with open('shaders/triangle_vtx.glsl', 'r') as vtx:
            vertex_src = vtx.read()

        with open('shaders/triangle_fr.glsl', 'r') as fr:
            fragment_src = fr.read()

        self._shader = compileProgram(compileShader(vertex_src, gl.GL_VERTEX_SHADER),
                                      compileShader(fragment_src, gl.GL_FRAGMENT_SHADER))

    def init_position(self):
        pos = gl.glGetAttribLocation(self._shader, "a_position")
        gl.glEnableVertexAttribArray(pos)
        gl.glVertexAttribPointer(pos, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, gl.ctypes.c_void_p(0))

    def init_color(self):
        color = gl.glGetAttribLocation(self._shader, "a_color")
        gl.glEnableVertexAttribArray(color)
        gl.glVertexAttribPointer(color, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, gl.ctypes.c_void_p(36))

    def draw(self):
        VBO = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, self._buffer.nbytes, self._buffer, gl.GL_STATIC_DRAW)

        self.init_position()
        self.init_color()

        gl.glUseProgram(self._shader)


# this triangle uses deprecated function calls and was just for testing
class deptriangle:

    def __init__(self, posx: vector3, posy: vector3, posz: vector3):
        self._vertices = [posx.tolist(),
                          posy.tolist(),
                          posz.tolist()]

        self._colors = [1.0, 0.0, 0.0,
                        0.0, 1.0, 0.0,
                        0.0, 0.0, 1.0]

        self._vertices = np.array(self._vertices, dtype=np.float32)
        self._colors = np.array(self._colors, dtype=np.float32)

    @staticmethod
    def animate(ct):
        gl.glLoadIdentity()
        gl.glScale(abs(sin(ct)), abs(sin(ct)), 7)
        gl.glRotatef(sin(ct) * 25, 0, 0, 1)
        gl.glTranslatef(sin(ct), cos(ct), 0)

    @staticmethod
    def draw():
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)

    def set_gl_settings(self):
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)
        gl.glVertexPointer(3, gl.GL_FLOAT, 0, self._vertices)
        gl.glColorPointer(3, gl.GL_FLOAT, 0, self._colors)


if __name__ == "__main__":
    window = openGlWindow(1280, 720, "Opengl Test Window A1")
    window.start()
