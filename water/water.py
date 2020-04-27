from OpenGL.GL import *
from shader import Shader
import callbacks as call
import camera as camera
import texture as tex
import utils as utils
import numpy as np
import inspect
import glm

N_POINTS: int = 256


def DEBUG():
    print(f"line {inspect.getframeinfo(inspect.stack()[1][0]).lineno:3}, error: {glGetError()}")


def create_grid(n_points: int):
    # gris_size = n_points x n_points
    vertices = np.empty((n_points, n_points, 3), dtype=np.float32)
    elements = list()
    for z, t in enumerate(np.linspace(-1.0, 1.0, n_points)):
        for x, s in enumerate(np.linspace(-1.0, 1.0, n_points)):
            vertices[x][z] = [s, 0, t]
            if x < n_points - 1 and z < n_points - 1:
                i = x + z * n_points
                elements.append([i, i + 1, i + n_points])
                elements.append([i + n_points, i + 1, i + n_points + 1])

    elements = np.array(elements, dtype=np.uint32)
    return vertices, elements


class Water:
    def __init__(self):
        self.updateShader = Shader(vertexShaderPath="./water/updateVertex.glsl",
                                   fragmentShaderPath="./water/updateFragment.glsl",
                                   shaderName="WaterUpdateShader")
        self.drawShader = Shader(vertexShaderPath="./water/drawVertex.glsl",
                                 fragmentShaderPath="./water/drawFragment.glsl",
                                 shaderName="WaterDrawShader")

        # Grid:
        self.vertices, self.elements = create_grid(N_POINTS)

        self.prevTex = tex.Texture(size=N_POINTS)
        self.currTex = tex.Texture(size=N_POINTS)
        self.nextTex = tex.Texture(size=N_POINTS)

        self.VAO, self.VBO, self.EBO = self.create_buffers()

        # Uniform location:
        self.MVPLoc = self.drawShader.getUniformLocation("MVP")
        self.modelLoc = self.drawShader.getUniformLocation("model")
        self.lightPosLoc = self.drawShader.getUniformLocation("lightPos")
        self.TrInvModelLoc = self.drawShader.getUniformLocation("TrInvModel")
        # Set model position:
        self.model = glm.mat4(1.0)
        self.model = glm.translate(self.model, glm.vec3(0.0, 0.3, 0.0))
        self.model = glm.scale(self.model, glm.vec3(1.0, 0.6, 1.0))
        self.model = glm.rotate(self.model, glm.radians(-70.0), glm.vec3(0.0, 1.0, 0.0))
        self.TrInvModel = glm.mat3(glm.transpose(glm.inverse(self.model)))

    def create_buffers(self):
        # Vertex Array Objects (VAO)
        VAO = glGenVertexArrays(1)
        glBindVertexArray(VAO)

        # Vertex Buffer Object (VBO)
        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER,
                     utils.sizeof(self.vertices),
                     self.vertices.ravel(),
                     GL_STATIC_DRAW)

        # Element Buffer Object (EBO)
        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,
                     utils.sizeof(self.elements),
                     self.elements.ravel(),
                     GL_STATIC_DRAW)

        #      'position' ----v
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, GLvoidp(0))
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)  # Unbind VBO
        glBindVertexArray(0)  # Unbind VAO

        return VAO, VBO, EBO

    def updateWater(self):
        VArgs = glGetIntegerv(GL_VIEWPORT)
        self.nextTex.bindFBO()
        self.nextTex.setViewport()
        glClear(GL_COLOR_BUFFER_BIT)

        # :--- [callback] ---:
        self.updateShader.use()
        # Uniform
        glUniform1i(self.updateShader.getUniformLocation("dropWater"), call.addRandomDrop())
        glUniform2f(self.updateShader.getUniformLocation("center"), *np.random.random(size=2))
        glUniform1f(self.updateShader.getUniformLocation("step"), 1.0 / self.nextTex.size)
        self.prevTex.bind()
        glUniform1i(self.updateShader.getUniformLocation("prevTexture"), self.prevTex.id)
        self.currTex.bind()
        glUniform1i(self.updateShader.getUniformLocation("currTexture"), self.currTex.id)
        self._draw()
        # :------------------:

        self.prevTex.unbind()
        self.currTex.unbind()
        self.nextTex.unbindFBO()
        glViewport(*VArgs)
        # Rotate
        self.prevTex, self.currTex, self.nextTex = \
            self.currTex, self.nextTex, self.prevTex

    def draw(self, lightPos):
        if not call.isSceneStopped():
            self.updateWater()

        # Options:
        if call.isSkeleton():
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.drawShader.use()
        # Uniform
        mvp = camera.get_projection_matrix() * \
              camera.get_view_matrix() * \
              self.model
        glUniformMatrix4fv(self.MVPLoc, 1, GL_FALSE, glm.value_ptr(mvp))
        glUniformMatrix4fv(self.modelLoc, 1, GL_FALSE, glm.value_ptr(self.model))
        glUniformMatrix3fv(self.TrInvModelLoc, 1, GL_FALSE, glm.value_ptr(self.TrInvModel))
        glUniform3f(self.lightPosLoc, lightPos.x, lightPos.y, lightPos.z)
        self.currTex.bind()
        glUniform1i(self.drawShader.getUniformLocation("heightMap"), self.currTex.id)
        glUniform1f(self.drawShader.getUniformLocation("step"), 1.0 / self.currTex.size)

        self._draw()

        self.currTex.unbind()
        glDisable(GL_BLEND)
        if call.isSkeleton():
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def _draw(self):
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, self.elements.size, GL_UNSIGNED_INT, GLvoidp(0))
        glBindVertexArray(0)  # Unbind VAO

    def __del__(self):
        glDeleteVertexArrays(1, [self.VAO])
        glDeleteBuffers(2, [self.VBO, self.EBO])
        del self.prevTex, self.currTex, self.nextTex
        del self.drawShader, self.updateShader
