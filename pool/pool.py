from OpenGL.GL import *
from shader import Shader
import camera as camera
import mesh.mesh as mesh
import utils
import glm


class Pool:
    def __init__(self):
        self.shader = Shader(vertexShaderPath="./pool/vertex.glsl",
                             fragmentShaderPath="./pool/fragment.glsl",
                             shaderName="PoolShader")

        self.texture = utils.create_texture(texturePath="./pool/pool.jpg")

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
        #       'texture' ----v
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, GLvoidp(12))
        glEnableVertexAttribArray(1)
        #        'normal' ----v
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 32, GLvoidp(20))
        glEnableVertexAttribArray(2)

        glBindBuffer(GL_ARRAY_BUFFER, 0)  # Unbind VBO
        glBindVertexArray(0)  # Unbind VAO

        # Uniform location
        self.MVPLoc = self.shader.getUniformLocation("MVP")
        self.modelLoc = self.shader.getUniformLocation("model")
        self.lightPosLoc = self.shader.getUniformLocation("lightPos")
        self.TrInvModelLoc = self.shader.getUniformLocation("TrInvModel")
        # Set model position
        self.model = glm.mat4(1.0)
        self.model = glm.scale(self.model, glm.vec3(1.0, 0.6, 1.0))
        self.model = glm.rotate(self.model, glm.radians(-70.0), glm.vec3(0.0, 1.0, 0.0))
        self.TrInvModel = glm.mat3(glm.transpose(glm.inverse(self.model)))

    def draw(self, lightPos):
        self.shader.use()
        # glPushAttrib(GL_ENABLE_BIT)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_FRONT)
        # Texture
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        # Uniform
        mvp = camera.get_projection_matrix() * \
              camera.get_view_matrix() * \
              self.model
        glUniformMatrix4fv(self.MVPLoc, 1, GL_FALSE, glm.value_ptr(mvp))
        glUniformMatrix4fv(self.modelLoc, 1, GL_FALSE, glm.value_ptr(self.model))
        glUniformMatrix3fv(self.TrInvModelLoc, 1, GL_FALSE, glm.value_ptr(self.TrInvModel))
        glUniform3f(self.lightPosLoc, lightPos.x, lightPos.y, lightPos.z)
        # Draw
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, mesh.cube.size)

        glBindVertexArray(0)  # Unbind VAO
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, 0)
        glDisable(GL_CULL_FACE)
        # glPopAttrib()

    def __del__(self):
        if hasattr(self, 'VAO'):
            glDeleteVertexArrays(1, [self.VAO])
        if hasattr(self, 'VBO'):
            glDeleteBuffers(1, [self.VBO])
        if hasattr(self, 'shader'):
            del self.shader
