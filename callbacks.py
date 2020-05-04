from OpenGL.GL import *
import camera as camera
import glfw
import glm

deltaTime: float = 0.0
lastFrame: float = 0.0

lastX = None
lastY = None

addRandomDrop: bool = False
rainActive: bool = True
rainSpeed: int = 100
maxRainSpeed: int = 10
minRainSpeed: int = 200
stepRainSpeed: int = 10
dropCoord = None

stopScene: bool = False
skeleton: bool = False
skybox: bool = False


def reset_time() -> None:
    global lastFrame, deltaTime
    currentFrame = glfw.get_time()
    deltaTime = currentFrame - lastFrame
    lastFrame = currentFrame


def rainSetting(key, action):
    global addRandomDrop, rainActive, rainSpeed
    if key == glfw.KEY_E and action == glfw.PRESS and not stopScene:
        addRandomDrop = True
        print("AddRandomDrop")

    if key == glfw.KEY_R and action == glfw.PRESS and not stopScene:
        rainActive = not rainActive
        rainSpeed = 100
        print(f"RainMode <{'ON' if rainActive else 'OFF'}>")

    if key == glfw.KEY_UP and action == glfw.PRESS and rainActive:
        rainSpeed = max(rainSpeed - stepRainSpeed, maxRainSpeed)
        if rainSpeed == maxRainSpeed:
            print("rainSpeed = MAX")
        else:
            print(f"rainSpeed = once per {rainSpeed} frames")

    if key == glfw.KEY_DOWN and action == glfw.PRESS and rainActive:
        rainSpeed = min(rainSpeed + stepRainSpeed, minRainSpeed)
        if rainSpeed == minRainSpeed:
            print("rainSpeed = MIN")
        else:
            print(f"rainSpeed = once per {rainSpeed} frames")


def key_callback(window, key, scancode, action, mode):
    global stopScene, skeleton, skybox
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

    rainSetting(key, action)

    if key == glfw.KEY_B and action == glfw.PRESS:
        skybox = not skybox
        print(f"CubemapMode <{'ON' if skybox else 'OFF'}>")

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


def counter(func):
    def wrap(*args, **kwargs):
        wrap.count += 1
        return func(*args, **kwargs)
    wrap.count = 0
    return wrap


@counter
def poll_events(window):
    global addRandomDrop
    addRandomDrop = False
    if rainActive:
        addRandomDrop = not (poll_events.count % rainSpeed)
    reset_time()
    camera_control(window)
    glfw.poll_events()
