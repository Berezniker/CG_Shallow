import callbacks as call
import glfw
import sys


class Window:
    def __init__(self, width: int, height: int, title: str):
        self.width = width
        self.height = height

        if not glfw.init():
            print("Failed to initialize GLFW", file=sys.stderr)
            exit(-1)

        glfw.window_hint(glfw.SAMPLES, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)  # for Mac OS X
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.CENTER_CURSOR, glfw.TRUE)

        self.window = glfw.create_window(
            width=width,
            height=height,
            title=title,
            monitor=None,
            share=None
        )

        if not self.window:
            print("Failed to open GLFW window", file=sys.stderr)
            glfw.terminate()
            exit(-1)

        glfw.make_context_current(self.window)
        glfw.swap_interval(1)  # V-Sync

    def set_callbacks(self):
        glfw.set_cursor_pos_callback(self.window, call.mouse_callback)
        glfw.set_scroll_callback(self.window, call.scroll_callback)
        glfw.set_key_callback(self.window, call.key_callback)

    def set_cursor(self):
        # glfw.create_cursor() ?
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    def isOpen(self) -> bool:
        return not glfw.window_should_close(self.window)

    def update(self):
        glfw.swap_buffers(self.window)

    def __del__(self):
        glfw.destroy_window(self.window)
        glfw.terminate()
