from OpenGL.GL import *
import numpy as np
import sys


class Texture:
    def __init__(self, size):
        self.size = size

        self.id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        data = np.zeros((self.size, self.size, 3), dtype=np.float32)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB32F, self.size, self.size, 0,
                     GL_RGB, GL_FLOAT, data)
        glBindTexture(GL_TEXTURE_2D, 0)  # Unbind texture

        self.FBO = glGenFramebuffers(1)  # Frame Buffer Objects
        glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0,
                               GL_TEXTURE_2D, self.id, 0)

        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print("Framebuffer is not complete!", file=sys.stderr)
            exit(-1)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

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
        glDeleteFramebuffers(1, [self.FBO])
