from OpenGL.GL import *
from shader import Shader
import camera as camera
import utils as utils
import numpy as np
import math
import glm

# based on http://www.songho.ca/opengl/gl_sphere.html


N_SECTOR = 25
N_STACK = 25


# latitude and longitude ~ sector and stacks
def create_sphere(nStack: int,
                  nSector: int,
                  radius: float = 1.0) -> np.array:
    vertices, textures, normals = list(), list(), list()
    sectorStep = 2.0 * math.pi / nSector
    stackStep = math.pi / nStack
    for i in range(nStack + 1):
        stackAngle = math.pi / 2.0 - i * stackStep
        xy = radius * math.cos(stackAngle)
        z = radius * math.sin(stackAngle)
        for j in range(nSector + 1):
            sectorAngle = j * sectorStep
            x = xy * math.cos(sectorAngle)
            y = xy * math.sin(sectorAngle)
            vertices.append([x, y, z])
            textures.append([j / nSector, i / nStack])
            normals.append([x / radius, y / radius, z / radius])

    vertices = np.array(vertices, dtype=np.float32).reshape((nStack + 1, nSector + 1, 3))
    textures = np.array(textures, dtype=np.float32).reshape((nStack + 1, nSector + 1, 2))
    normals = np.array(normals, dtype=np.float32).reshape((nStack + 1, nSector + 1, 3))
    return vertices, textures, normals


def sphere_triangulation(nStack: int,
                         nSector: int) -> np.array:
    """
    k1 <- k1+1
     |  / / ^
     v / /  |
    k2 -> k2+1
    """
    elements = list()
    for i in range(nStack):
        k1 = i * (nSector + 1)
        k2 = k1 + nSector + 1
        for j in range(nSector):
            if i != 0:
                elements.append([k1, k2, k1 + 1])
            if i != nStack - 1:
                elements.append([k1 + 1, k2, k2 + 1])
            k1 += 1
            k2 += 1

    return np.array(elements, dtype=np.uint32)


class Sphere:
    def __init__(self):
        self.shader = Shader(vertexShaderPath="./sphere/vertex.glsl",
                             fragmentShaderPath="./sphere/fragment.glsl",
                             shaderName="SphereShader")

        self.texture = utils.create_texture(texturePath="./sphere/moon.jpg")

        vertices, textures, normals = create_sphere(N_STACK, N_SECTOR)
        self.vertices = np.dstack((vertices, textures, normals))
        self.elements = sphere_triangulation(N_STACK, N_SECTOR)

        # Vertex Array Objects (VAO)
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        # Vertex Buffer Object (VBO)
        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER,
                     utils.sizeof(self.vertices),
                     self.vertices.ravel(),
                     GL_STATIC_DRAW)

        # Element Buffer Object (EBO)
        self.EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER,
                     utils.sizeof(self.elements),
                     self.elements.ravel(),
                     GL_STATIC_DRAW)

        #      'position' ----v
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, GLvoidp(0))
        glEnableVertexAttribArray(0)
        #       'texture' ----v
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, GLvoidp(12))
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
        self.model = glm.translate(self.model, glm.vec3(0.4, -0.25, 0))
        self.model = glm.scale(self.model, glm.vec3(0.25))
        self.model = glm.rotate(self.model, glm.radians(90.0), glm.vec3(1.0, 0.0, 0.0))
        self.TrInvModel = glm.mat3(glm.transpose(glm.inverse(self.model)))

    def draw(self, lightPos):
        self.shader.use()
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
        glDrawElements(GL_TRIANGLES, self.elements.size, GL_UNSIGNED_INT, None)
        glBindVertexArray(0)  # Unbind VAO
        # Unbind texture
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, 0)

    def __del__(self):
        if hasattr(self, 'VAO'):
            glDeleteVertexArrays(1, [self.VAO])
        if hasattr(self, 'VBO'):
            glDeleteBuffers(1, [self.VBO])
        if hasattr(self, 'EBO'):
            glDeleteBuffers(1, [self.EBO])
        if hasattr(self, 'shader'):
            del self.shader
