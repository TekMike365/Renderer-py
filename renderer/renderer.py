from types import FunctionType
from typing import Any
from .camera import Camera
from .vmath import Mat4, Vec2, Vec3, Vec4
from .bitmap import make_bitmap


def triangle_lerp(
    p1: tuple[Vec2, float], p2: tuple[Vec2, float], p3: tuple[Vec2, float], point: Vec2
) -> float:
    # Calculate the barycentric coordinates of the point inside the triangle
    u = (
        (p2[0].y - p3[0].y) * (point.x - p3[0].x)
        + (p3[0].x - p2[0].x) * (point.y - p3[0].y)
    ) / (
        (p2[0].y - p3[0].y) * (p1[0].x - p3[0].x)
        + (p3[0].x - p2[0].x) * (p1[0].y - p3[0].y)
    )
    v = (
        (p1[0].y - p2[0].y) * (point.x - p2[0].x)
        + (p2[0].x - p1[0].x) * (point.y - p2[0].y)
    ) / (
        (p2[0].y - p3[0].y) * (p1[0].x - p3[0].x)
        + (p3[0].x - p2[0].x) * (p1[0].y - p3[0].y)
    )
    w = 1 - u - v

    # Interpolate the values based on the barycentric coordinates
    interpolated_value = p1[1] * u + p2[1] * v + p3[1] * w

    return interpolated_value


vertex_buffer: list[list[Any]] = []
index_buffer: list = []
uniform_buffer: list = []
vertex_shader: FunctionType | None = None
fragment_shader: FunctionType | None = None
screen_buffer: list[int] = []
depth_buffer: list[float] = []
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

        # get positions
        vp1, vp2, vp3 = vert_shader_outs
        p1 = Vec2(
            (vp1[0].x + 2) / 2 * screen_size.x, (vp1[0].y + 2) / 2 * screen_size.y
        )
        p2 = Vec2(
            (vp2[0].x + 2) / 2 * screen_size.x, (vp2[0].y + 2) / 2 * screen_size.y
        )
        p3 = Vec2(
            (vp3[0].x + 2) / 2 * screen_size.x, (vp3[0].y + 2) / 2 * screen_size.y
        )
        bounding_box_min = Vec2(min(p1.x, p2.x, p3.x), min(p1.y, p2.y, p3.y))
        bounding_box_max = Vec2(max(p1.x, p2.x, p3.x), max(p1.y, p2.y, p3.y))
        # culling l1
        if (
            bounding_box_min.x < 0
            or bounding_box_min.y < 0
            or bounding_box_max.x > screen_size.x
            or bounding_box_max.y > screen_size.y
        ):
            continue

        for y in range(int(bounding_box_min.y), int(bounding_box_max.y + 1)):
            # culling l2
            if y > screen_size.y:
                break

            for x in range(int(bounding_box_min.x), int(bounding_box_max.x + 1)):
                # culling l3
                if x > screen_size.x:
                    break

                # calculating depth
                point = Vec2(x, y)
                depth = triangle_lerp(
                    (p1, vp1[0].z), (p2, vp2[0].z), (p3, vp3[0].z), point
                )

                # culling l4
                if depth > depth_buffer[y * int(screen_size.x) + x]:
                    continue

                # TODO: interpolate vert_shader_outs
                lerped_vert_shader_outs = []

                # TODO: color = fragment_shader(vert_shader_outs[1:], uniform_buffer)
                pass

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
    global clear_color, screen_buffer, depth_buffer
    screen_buffer = [int(clear_color.x), int(clear_color.y), int(clear_color.z)] * int(
        screen_size.x * screen_size.y
    )
    depth_buffer = [1e100, 1e100, 1e100] * int(screen_size.x * screen_size.y)


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
