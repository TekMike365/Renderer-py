from typing import Any
import renderer as re

# Define vertices of the cube
vertices = [
    [re.Vec3(-0.5, -0.5, -0.5), re.Vec3(0.0, 1.0, 0.0)],
    [re.Vec3( 0.5, -0.5, -0.5), re.Vec3(0.0, 0.0, 1.0)],
    [re.Vec3( 0.5, -0.5,  0.5), re.Vec3(1.0, 1.0, 1.0)],
    [re.Vec3(-0.5, -0.5,  0.5), re.Vec3(1.0, 1.0, 1.0)],

    [re.Vec3(-0.5,  0.5, -0.5), re.Vec3(1.0, 0.0, 0.0)],
    [re.Vec3( 0.5,  0.5, -0.5), re.Vec3(1.0, 1.0, 1.0)],
    [re.Vec3( 0.5,  0.5,  0.5), re.Vec3(1.0, 1.0, 1.0)],
    [re.Vec3(-0.5,  0.5,  0.5), re.Vec3(1.0, 1.0, 1.0)],
]

# Define indices for triangles forming the cube
indices = [
    # front
    0, 1, 5,
    5, 4, 0,
    # right
    # 1, 2, 6,
    # 6, 5, 1,
    # back
    # 2, 3, 7,
    # 7, 6, 2,
    # left
    # 3, 0, 4,
    # 4, 7, 3,
    # top
    # 6, 7, 4,
    # 4, 5, 6,
    # bottom
    # 1, 0, 3,
    # 3, 2, 1,
]

re.set_screen_size(re.Vec2(640, 420))

camera = re.Camera(45.0, re.Vec2(1.0, 4.8 / 6.4))
camera.translate(re.Vec3(1.0, 0.0, -1.5))

re.upload_uniform(camera, "camera")


def vertex_shader(atribs: list[Any], uniforms: dict) -> list[Any]:
    a_pos: re.Vec3 = atribs[0]
    a_color: re.Vec3 = atribs[1]
    camera: re.Camera = uniforms["camera"]

    pos = a_pos
    #pos = camera.world2screen_pos(a_pos)

    return [pos, a_color]


def fragment_shader(vout: list[Any], uniforms: dict) -> re.Vec3:
    v_color = vout[0]
    return v_color


re.upload_vertex_shader_fn(vertex_shader)
re.upload_fragment_shader_fn(fragment_shader)

re.upload_vertex_buffer(vertices)
re.upload_index_buffer(indices)

re.clear_screen()
re.draw_triangles()
re.save("cube.bmp")

re.upload_index_buffer([
    # front
    # 0, 1, 5,
    # 5, 4, 0,
    # right
    # 1, 2, 6,
    # 6, 5, 1,
    # back
    # 2, 3, 7,
    # 7, 6, 2,
    # left
    # 3, 0, 4,
    # 4, 7, 3,
    # top
    # 6, 7, 4,
    # 4, 5, 6,
    # bottom
    # 1, 0, 3,
    # 3, 2, 1,
])
re.clear_screen()
re.draw_triangles()
re.save("cube1.bmp")
