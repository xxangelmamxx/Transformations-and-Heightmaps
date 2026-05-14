#version 330 core

out vec4 fragColor;
in vec2 texCoords; // Receive 2D texture coordinates

uniform sampler2D u_texture_skybox; // Use sampler2D instead of samplerCube

void main() {
    fragColor = texture(u_texture_skybox, texCoords); // Sample texture using 2D coordinates
}
