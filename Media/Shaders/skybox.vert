#version 330 core

layout (location = 0) in vec3 in_position; // 3D position of the vertex
layout (location = 1) in vec2 in_texcoord; // 2D texture coordinates

out vec2 texCoords; // Pass the texture coordinates to the fragment shader

uniform mat4 m_proj;
uniform mat4 m_view;

void main() {
    texCoords = in_texcoord; // Pass texture coordinates to the fragment shader
    mat4 viewNoTranslation = mat4(mat3(m_view)); // Remove translation from view matrix
    vec4 pos = m_proj * viewNoTranslation * vec4(in_position, 1.0);
    gl_Position = pos.xyww; // Use .xyww to keep the correct perspective
    gl_Position.z -= 0.0001; // Offset to prevent Z-fighting
}
