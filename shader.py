from OpenGL.GL import *
import sys


def load_shader(shaderName: str):
    code: str = ""
    try:
        with open(file=shaderName, mode='r') as f:
            for line in f:
                code += line
    except Exception as e:
        print(e, file=sys.stderr)
        exit(-1)

    return code


def create_shader(shaderType, sourceCode: str):
    shader = glCreateShader(shaderType)
    glShaderSource(shader, sourceCode)
    glCompileShader(shader)

    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        print(f"{shaderType}:\n{glGetShaderInfoLog(shader)}", file=sys.stderr)
        exit(-1)

    return shader


def link_program(vertexShader, fragmentShader):
    program = glCreateProgram()
    glAttachShader(program, vertexShader)
    glAttachShader(program, fragmentShader)
    glLinkProgram(program)

    if not glGetProgramiv(program, GL_LINK_STATUS):
        print(f"Link status:\n{glGetProgramInfoLog(program)}", file=sys.stderr)
        exit(-1)

    glDeleteShader(vertexShader)
    glDeleteShader(fragmentShader)

    return program


class Shader:
    def __init__(self, vertexShaderPath: str,
                 fragmentShaderPath: str,
                 shaderName: str = None):
        vertexCode = load_shader(vertexShaderPath)
        fragmentCode = load_shader(fragmentShaderPath)

        vertexShader = create_shader(GL_VERTEX_SHADER, vertexCode)
        fragmentShader = create_shader(GL_FRAGMENT_SHADER, fragmentCode)

        self.program = link_program(vertexShader, fragmentShader)
        self.name = shaderName
        if shaderName is None:
            self.name = f"Shader[{self.program}]"

    def getUniformLocation(self, name: str):
        loc = glGetUniformLocation(self.program, name)
        if loc == -1:
            print(f"{self}: location {name} not found", file=sys.stderr)
        return loc

    def use(self):
        glUseProgram(self.program)

    def __str__(self):
        return self.name

    def __del__(self):
        if hasattr(self, 'program'):
            glDeleteProgram(self.program)
