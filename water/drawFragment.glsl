#version 330 core

in vec3 vFragPos;
in vec3 vNormal;

uniform vec3 cameraPos;
uniform samplerCube skybox;

void main() {
    float ratio = 1.0 / 1.33;
    vec3 I = normalize(vFragPos - cameraPos);
    vec3 R = reflect(I, normalize(vNormal));
    // vec3 R = refract(I, normalize(vNormal), ratio);
    gl_FragColor = vec4(texture(skybox, R).rgb, 0.8);
}
