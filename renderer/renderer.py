from types import FunctionType
from typing import Any
from .camera import Camera
from .vmath import Mat4, Vec2, Vec3, Vec4
from .bitmap import make_bitmap

vertex_buffer: list[list[Any]] = []
index_buffer: list = []
uniform_buffer: list = []
vertex_shader: FunctionType | None = None
fragment_shader: FunctionType | None = None
screen_buffer: list[int] = []
clear_color: Vec3 = Vec3(0, 0, 0)
screen_size: Vec2 = Vec2(640, 420)


def draw_triangles():
    if vertex_shader is None or fragment_shader is None:
        return

    iidxs = 0
    while iidxs < len(index_buffer):
        indices = index_buffer[iidxs : iidxs + 3]
        vert_shader_outs: list[list[Any]] = []

        for i in indices:
            vert_shader_outs += [vertex_shader(vertex_buffer[i], uniform_buffer)]

        # TODO: interpolate vert_shader_outs
        # TODO: color = fragment_shader(vert_shader_outs[1:], uniform_buffer)

        iidxs += 3


def upload_vertex_shader(shader: FunctionType) -> None:
    global vertex_shader
    vertex_shader = shader


def upload_fragment_shader(shader: FunctionType) -> None:
    global fragment_shader
    fragment_shader = shader


def set_clear_color(color: Vec3) -> None:
    global clear_color
    clear_color = color


def set_screen_size(size: Vec2) -> None:
    global screen_size
    screen_size = size


def clear_screen() -> None:
    global clear_color, screen_buffer
    screen_buffer = [int(clear_color.x), int(clear_color.y), int(clear_color.z)] * int(
        screen_size.x * screen_size.y
    )


def upload_vertex_buffer(buffer: list) -> None:
    global vertex_buffer
    vertex_buffer = buffer


def upload_index_buffer(buffer: list) -> None:
    global index_buffer
    index_buffer = buffer


def upload_uniform(val: Any) -> None:
    global uniform_buffer
    uniform_buffer += [val]


def save(filepath: str) -> None:
    make_bitmap(filepath, int(screen_size.x), int(screen_size.y), screen_buffer)
