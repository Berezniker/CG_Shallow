import math
import glm

width: int = 800
height: int = 600

position = glm.vec3(-0.4, 0.9, 2.2)
up = glm.vec3(0.0, 1.0, 0.0)
fov = 45.0  # field of view

pitch: float = -22.0
yaw: float = -78.0

front = glm.normalize(glm.vec3(
        math.cos(glm.radians(pitch)) * math.cos(glm.radians(yaw)),
        math.sin(glm.radians(pitch)),
        math.cos(glm.radians(pitch)) * math.sin(glm.radians(yaw))
    ))


def updateFront():
    global front
    front = glm.normalize(glm.vec3(
        math.cos(glm.radians(pitch)) * math.cos(glm.radians(yaw)),
        math.sin(glm.radians(pitch)),
        math.cos(glm.radians(pitch)) * math.sin(glm.radians(yaw))
    ))


def get_view_matrix():
    return glm.lookAt(position, position + front, up)


def get_projection_matrix():
    return glm.perspective(glm.radians(fov), width / height, 0.1, 100.0)


def setF1Location():
    global position, pitch, yaw
    position = glm.vec3(-0.4, 0.9, 2.2)
    pitch = -22.0
    yaw = -78.0
    updateFront()


def setF2Location():
    global position, pitch, yaw
    position = glm.vec3(0.42, -0.45, -1.05)
    pitch = 22.0
    yaw = 112.0
    updateFront()


def setF3Location():
    global position, pitch, yaw
    position = glm.vec3(-3.12, 3.83, 3.93)
    pitch = -38.0
    yaw = -53.0
    updateFront()
