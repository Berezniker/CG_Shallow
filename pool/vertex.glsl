#version 330 core

layout(location=0) in vec3 position;
layout(location=1) in vec2 texture;
layout(location=2) in vec3 normal;

uniform mat4 MVP;
uniform mat4 model;
uniform mat3 TrInvModel;

out vec3 vFragPos;
out vec3 vNormal;
out vec2 vUV;

void main() {
    gl_Position = MVP * vec4(position, 1.0);
    vFragPos = vec3(model * vec4(position, 1.0));
    vNormal = - TrInvModel * normal;
    vUV = texture;
}
