from typing import Any
import renderer as re

re.set_screen_size(re.Vec2(640, 420))

camera = re.Camera(45.0, re.Vec2(1.0, 4.8 / 6.4))
camera.translate(re.Vec3(1.0, 0.0, -1.0))

re.upload_uniform(camera, "camera")


def vertex_shader(atribs: list[Any], uniforms: dict) -> list[Any]:
    a_pos: re.Vec3 = atribs[0]
    a_color: re.Vec3 = atribs[1]
    camera: re.Camera = uniforms["camera"]

    pos = camera.world2screen_pos(a_pos)

    return [pos, a_color]


def fragment_shader(vout: list[Any], uniforms: dict) -> re.Vec3:
    v_color: re.Vec3 = vout[0]
    return v_color


re.upload_vertex_shader_fn(vertex_shader)
re.upload_fragment_shader_fn(fragment_shader)

re.upload_vertex_buffer(
    [
        [re.Vec3(0.0, 0.5, 0.0), re.Vec3(1.0, 0.0, 0.0)],
        [re.Vec3(-0.5, -0.5, 0.0), re.Vec3(0.0, 1.0, 0.0)],
        [re.Vec3(0.5, -0.5, 0.0), re.Vec3(0.0, 0.0, 1.0)],
    ]
)
re.upload_index_buffer([0, 1, 2])

re.clear_screen()
re.draw_triangles()
re.save("triangle.bmp")
