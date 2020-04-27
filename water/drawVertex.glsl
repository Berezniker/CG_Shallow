#version 330 core

layout(location=0) in vec3 position;

uniform sampler2D heightMap;
uniform float step;
uniform mat4 MVP;
uniform mat4 model;
uniform mat3 TrInvModel;

out vec3 vFragPos;
out vec3 vNormal;

void main() {
    vec2 coord = 0.5 * position.xz + 0.5; // [-1.0, 1.0] to [0.0, 1.0]
    float h = texture2D(heightMap, coord).y;
    gl_Position = MVP * vec4(position.x, h, position.z, 1.0);
    vFragPos = vec3(model * vec4(position.x, h, position.z, 1.0));

    vec3 dx = vec3(step, texture2D(heightMap, vec2(coord.x + step, coord.y)).y - h, 0.0);
    vec3 dz = vec3(0.0, texture2D(heightMap, vec2(coord.x, coord.y + step)).y - h, step);
    vNormal = normalize(cross(dz, dx));
    vNormal = TrInvModel * vNormal;
    vNormal = normalize(vNormal);
}
