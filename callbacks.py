from OpenGL.GL import *
import camera as camera
import glfw
import glm

deltaTime: float = 0.0
lastFrame: float = 0.0

lastX = None
lastY = None

stopScene: bool = False
waterDrop: bool = False
skeleton: bool = False


def reset_time():
    global lastFrame, deltaTime
    currentFrame = glfw.get_time()
    deltaTime = currentFrame - lastFrame
    lastFrame = currentFrame


def isSceneStopped() -> bool:
    return stopScene


def isSkeleton() -> bool:
    return skeleton


def addRandomDrop() -> bool:
    return waterDrop


def key_callback(window, key, scancode, action, mode):
    global stopScene, skeleton, waterDrop
    # NOTE! You need to run with the ENGLISH layout, not otherwise
    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, GL_TRUE)
        return

    if key == glfw.KEY_F1 and action == glfw.PRESS:
        camera.setF1Location()
    if key == glfw.KEY_F2 and action == glfw.PRESS:
        camera.setF2Location()
    if key == glfw.KEY_F3 and action == glfw.PRESS:
        camera.setF3Location()

    if key == glfw.KEY_F5 and action == glfw.PRESS:
        stopScene = not stopScene
        print(f"Scene <{'stop' if stopScene else 'run'}>")

    if key == glfw.KEY_Q and action == glfw.PRESS:
        skeleton = not skeleton
        print(f"WaterPolygonMode <{'ON' if skeleton else 'OFF'}>")

    if key == glfw.KEY_R and action == glfw.PRESS and not stopScene:
        waterDrop = True
        print("AddRandomDrop")

    # DEBUG
    # print(f"position={camera.position}")


def mouse_callback(window, xpos, ypos):
    global lastX, lastY
    lastX = lastX if lastX is not None else xpos
    lastY = lastY if lastY is not None else ypos
    offsetX = xpos - lastX
    offsetY = lastY - ypos
    lastX, lastY = xpos, ypos

    mouseSensitivity: float = 0.10
    offsetX *= mouseSensitivity
    offsetY *= mouseSensitivity
    camera.yaw += offsetX
    camera.pitch += offsetY
    camera.pitch = max(-89.0, min(89.0, camera.pitch))
    camera.updateFront()

    # DEBUG
    # print(f"yaw={camera.yaw}, pitch={camera.pitch}")


def scroll_callback(window, xoffset, yoffset):
    if 1.0 <= camera.fov <= 45.0:
        camera.fov -= yoffset
    camera.fov = max(1.0, min(45.0, camera.fov))


def camera_control(window):
    cameraSpeed = 1 * deltaTime
    # Camera controls
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        camera.position += cameraSpeed * camera.front
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        camera.position -= cameraSpeed * camera.front
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        camera.position -= glm.normalize(glm.cross(camera.front, camera.up)) \
                           * cameraSpeed
    if glfw.get_key(window, glfw.KEY_D):
        camera.position += glm.normalize(glm.cross(camera.front, camera.up)) \
                           * cameraSpeed


def poll_events(window):
    global waterDrop
    waterDrop = False
    reset_time()
    camera_control(window)
    glfw.poll_events()
