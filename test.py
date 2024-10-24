from typing import Any
import renderer as re

# Define vertices of the cube
vertices = [
    [re.Vec3(-0.5, -0.5, -0.5)],
    [re.Vec3(0.5, -0.5, -0.5)],
    [re.Vec3(0.5, 0.5, -0.5)],
    [re.Vec3(-0.5, 0.5, -0.5)],
    [re.Vec3(-0.5, -0.5, 0.5)],
    [re.Vec3(0.5, -0.5, 0.5)],
    [re.Vec3(0.5, 0.5, 0.5)],
    [re.Vec3(-0.5, 0.5, 0.5)],
]

# Define indices for triangles forming the cube
indices = [
    0,
    1,
    2,
    2,
    3,
    0,
    4,
    5,
    6,
    6,
    7,
    4,
    0,
    1,
    5,
    5,
    4,
    0,
    1,
    2,
    6,
    6,
    5,
    1,
    2,
    3,
    7,
    7,
    6,
    2,
    3,
    0,
    4,
    4,
    7,
    3,
]

re.set_screen_size(re.Vec2(640, 420))

camera = re.Camera(45.0, re.Vec2(6.4, 4.8))
camera.translate(re.Vec3(0.0, 0.0, -3.0))

re.upload_uniform(camera, "camera")


def vertex_shader(atribs: list[Any], uniforms: dict) -> list[Any]:
    a_pos: re.Vec3 = atribs[0]
    camera: re.Camera = uniforms["camera"]

    pos = camera.world2screen_pos(a_pos)

    return [pos]


def fragment_shader(vout: list[Any], uniforms: dict) -> re.Vec3:
    return re.Vec3(255, 255, 255)


re.upload_vertex_shader_fn(vertex_shader)
re.upload_fragment_shader_fn(fragment_shader)

re.upload_vertex_buffer(vertices)
re.upload_index_buffer(indices)

re.clear_screen()
re.draw_triangles()
