from OpenGL.GL import *

from sphere.sphere import Sphere
from water.water import Water
from light.light import Light
from pool.pool import Pool
from window import Window
import camera as camera
import callbacks as call


def main():
    window = Window(width=camera.width,
                    height=camera.height,
                    title='Shallow')
    window.set_callbacks()

    pool = Pool()
    light = Light()
    water = Water()
    sphere = Sphere()

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
        light.draw()
        pool.draw(light.position)
        sphere.draw(light.position)
        water.draw(light.position)
        # ------------
        window.update()

    del pool, light, water, sphere, window


if __name__ == "__main__":
    main()
