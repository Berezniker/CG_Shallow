from OpenGL.GL import *

from cubemap.cubemap import Cubemap
from sphere.sphere import Sphere
from water.water import Water
from pool.pool import Pool
from window import Window
import callbacks as call
import camera
import glm

LIGHT_POSITION = glm.vec3(-3.0, 3.0, 3.0)


def main():
    window = Window(width=camera.width,
                    height=camera.height,
                    title='Shallow')
    window.set_callbacks()
    window.set_cursor()

    pool = Pool()
    water = Water()
    sphere = Sphere()
    cubemap = Cubemap()

    # Options:
    glViewport(0, 0, camera.width, camera.height)
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glFrontFace(GL_CCW)

    # DEBUG
    # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    while window.isOpen():
        # Check if any events have been activated:
        call.poll_events(window.window)
        # Render
        #           |-------------| <- background color
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # --- Draw ---
        pool.draw(LIGHT_POSITION)
        sphere.draw(LIGHT_POSITION)
        water.draw(camera.position,
                   cubemap.id)
        if call.skybox:
            cubemap.draw()
        # ------------
        window.update()

    del window, pool, sphere, water


if __name__ == "__main__":
    main()
