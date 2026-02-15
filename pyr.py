"""
ImageBuffer
VertexBuffer
IndexBuffer
UniformBuffer

Shader

Camera
Transform
...

Model: (vertices, indices, textures, ...)
Scene: (models, camera, ...)

Renderer:
    - renders scene to an image with given shader
    - invokes compute shaders
"""

# from PIL import Image, ImageDraw # image drawing
import numpy as np # vectors

# creates a perspective matrix
def perspective(fov_deg, aspect, near, far):
    mat = np.eye(4)

    fov_rad = np.radians(fov_deg)
    f = 1.0 / np.tan(fov_rad / 2.0)

    mat[0, 0] = f / aspect
    mat[1, 1] = f
    mat[2, 2] = -1 / (far - near)
    mat[2, 3] = -near / (far - near)
    mat[3, 2] = -1.0

    return mat

def translation(mat4, pos3):
    mat4[0, 3] = pos3[0]
    mat4[1, 3] = pos3[1]
    mat4[2, 3] = pos3[2]
    return mat4

if __name__ == "__main__":
    width, height = 640, 480

    vertices = [
        np.array([ 0.5, -0.5, 0.0]),
        np.array([ 0.0,  0.5, 0.0]),
        np.array([-0.5, -0.5, 0.0])
    ]
    indices = [0, 1, 2]

    persp = perspective(90, width / height, 0.1, 100.0)
    pos = translation(np.eye(4), [0.0, 0.0, -1.0])

    vpmat = persp @ pos

    pts = [np.append(p, 1.0) for p in vertices]
    pts = [vpmat @ p for p in pts]
    pts = [p[:3] / p[3] for p in pts]

