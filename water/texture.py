from OpenGL.GL import *
import numpy as np
import sys


def DEBUG():
    import inspect
    print(f"line {inspect.getframeinfo(inspect.stack()[1][0]).lineno:3}, error: {glGetError()}")


class Texture:
    def __init__(self, size):
        self.size = size

        self.id = glGenTextures(1)
        DEBUG()
        glBindTexture(GL_TEXTURE_2D, self.id)
        DEBUG()
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        DEBUG()
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        DEBUG()
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        DEBUG()
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        DEBUG()
        data = np.zeros((self.size, self.size, 4), dtype=np.float32)
        DEBUG()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, self.size, self.size, 0,
                     GL_RGBA, GL_FLOAT, data)
        DEBUG()
        glBindTexture(GL_TEXTURE_2D, 0)  # Unbind texture
        DEBUG()
        self.FBO = glGenFramebuffers(1)  # Frame Buffer Objects
        DEBUG()
        glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)
        DEBUG()
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0,
                               GL_TEXTURE_2D, self.id, 0)
        DEBUG()
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print("Framebuffer is not complete!", file=sys.stderr)
            exit(-1)
        DEBUG()
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        DEBUG()

    def bind(self):
        glActiveTexture(GL_TEXTURE0 + self.id)
        glBindTexture(GL_TEXTURE_2D, self.id)

    def unbind(self):
        glActiveTexture(GL_TEXTURE0 + self.id)
        glBindTexture(GL_TEXTURE_2D, 0)

    def bindFBO(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0,
                               GL_TEXTURE_2D, self.id, 0)

    def unbindFBO(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def setViewport(self):
        glViewport(0, 0, self.size, self.size)

    def __del__(self):
        if hasattr(self, 'EBO'):
            glDeleteBuffers(1, [self.EBO])
