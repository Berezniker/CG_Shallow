from OpenGL.GL import *
from shader import Shader
import camera as camera
import mesh.mesh as mesh
import utils as utils
import glm


class Light:
    def __init__(self, position=glm.vec3(-3.0, 3.0, 3.0)):
        self.position = position
        self.shader = Shader(vertexShaderPath="./light/vertex.glsl",
                             fragmentShaderPath="./light/fragment.glsl",
                             shaderName="LightShader")

        # Vertex Array Objects (VAO)
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        # Vertex Buffer Object (VBO)
        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER,
                     utils.sizeof(mesh.cube),
                     mesh.cube,
                     GL_STATIC_DRAW)

        #      'position' ----v
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, GLvoidp(0))
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)  # Unbind VBO
        glBindVertexArray(0)  # Unbind VAO

        # Uniform location
        self.MVPLoc = self.shader.getUniformLocation("MVP")
        # Set model position
        self.model = glm.mat4(1.0)
        self.model = glm.translate(self.model, self.position)
        self.model = glm.scale(self.model, glm.vec3(0.1, 0.1, 0.1))

    def draw(self):
        self.shader.use()
        # Uniform
        mvp = camera.get_projection_matrix() * \
              camera.get_view_matrix() * \
              self.model
        glUniformMatrix4fv(self.MVPLoc, 1, GL_FALSE, glm.value_ptr(mvp))
        # Draw
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, mesh.cube.size)
        glBindVertexArray(0)  # Unbind VAO

    def __del__(self):
        glDeleteVertexArrays(1, [self.VAO])
        glDeleteBuffers(1, [self.VBO])
        del self.shader
