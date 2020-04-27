#version 330 core

in vec3 vFragPos;
in vec3 vNormal;

uniform vec3 lightPos;

void main() {
    vec3 norm = normalize(vNormal);
    vec3 lightDir = normalize(lightPos - vFragPos);
    vec4 diffuse = vec4(vec3(max(dot(norm, lightDir), 0.0)), 1.0);

    vec4 objectColor = vec4(0.0, 0.58, 0.71, 0.7);
    vec4 ambient = objectColor * 0.1;

    // gl_FragColor = vec4(vNormal, 1.0);
    gl_FragColor = (ambient + diffuse) * objectColor;
}
