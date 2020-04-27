#version 330 core

layout(location=0) in vec3 position;

out vec2 coord;

void main() {
    coord = 0.5 * position.xz + 0.5; // [-1.0, 1.0] to [0.0, 1.0]
    gl_Position = vec4(position.xz, 0.0, 1.0);
}
