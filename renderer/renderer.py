from typing import Any
from .vmath import Mat4, Vec2, Vec3, Vec4
from .bitmap import make_bitmap


def lerp(v1: float, v2: float, t: float) -> float:
    return (1 - t) * v1 + t * v2


def tlerp(v1: float, v2: float, v3: float, t: float, s: float) -> float:
    i = lerp(v1, v2, t)
    return lerp(v3, i, s)


def triangle_lerp(
    vp1: tuple[Vec2, float], vp2: tuple[Vec2, float], vp3: tuple[Vec2, float], pt: Vec2
) -> float:
    p1, v1 = vp1
    p2, v2 = vp2
    p3, v3 = vp3

    va = p2.copy().sub(p1)
    vc = pt.copy().sub(p3)

    b = vc.y * (p1.x - p3.x) - vc.x * (p1.y - p3.y)
    a = vc.y * va.x - vc.x * va.y

    if a == 0:
        return 0

    t = -b / a

    vi = p1.copy().add(va.copy().scale(t))
    i = lerp(v1, v2, t)

    vn = vi.copy().sub(p3)

    if vn.get_scale() == 0:
        return 0

    s = vc.get_scale() / vn.get_scale()

    return lerp(v3, i, s)


def triangle_lerp_any(
    vp1: tuple[Vec2, Any], vp2: tuple[Vec2, Any], vp3: tuple[Vec2, Any], point: Vec2
) -> Any:
    p1, v1 = vp1
    p2, v2 = vp2
    p3, v3 = vp3
    vp_type = type(v1)
    if vp_type is float:
        return triangle_lerp((p1, v1), (p2, v2), (p3, v3), point)
    elif isinstance(vp_type, int):
        return int(
            triangle_lerp((p1, float(v1)), (p2, float(v2)), (p3, float(v3)), point)
        )
    elif vp_type is Vec2:
        ivx = triangle_lerp((p1, v1.x), (p2, v2.x), (p3, v3.x), point)
        ivy = triangle_lerp((p1, v1.y), (p2, v2.y), (p3, v3.y), point)
        return Vec2(ivx, ivy)
    elif vp_type is Vec3:
        ivx = triangle_lerp((p1, v1.x), (p2, v2.x), (p3, v3.x), point)
        ivy = triangle_lerp((p1, v1.y), (p2, v2.y), (p3, v3.y), point)
        ivz = triangle_lerp((p1, v1.z), (p2, v2.z), (p3, v3.z), point)
        return Vec3(ivx, ivy, ivz)
    elif vp_type is Vec4:
        ivx = triangle_lerp((p1, v1.x), (p2, v2.x), (p3, v3.x), point)
        ivy = triangle_lerp((p1, v1.y), (p2, v2.y), (p3, v3.y), point)
        ivz = triangle_lerp((p1, v1.z), (p2, v2.z), (p3, v3.z), point)
        ivw = triangle_lerp((p1, v1.w), (p2, v2.w), (p3, v3.w), point)
        return Vec4(ivx, ivy, ivz, ivw)
    elif vp_type is Mat4:
        iv1 = triangle_lerp_any((p1, v1.c1), (p2, v2.c1), (p2, v2.c1), point)
        iv2 = triangle_lerp_any((p1, v1.c2), (p2, v2.c2), (p2, v2.c2), point)
        iv3 = triangle_lerp_any((p1, v1.c3), (p2, v2.c3), (p2, v2.c3), point)
        iv4 = triangle_lerp_any((p1, v1.c4), (p2, v2.c4), (p2, v2.c4), point)
        mat = Mat4()
        mat.c1 = iv1
        mat.c2 = iv2
        mat.c3 = iv3
        mat.c4 = iv4
        return mat


def is_in_triangle(p1: Vec2, p2: Vec2, p3: Vec2, point: Vec2) -> bool:
    v1 = p1.copy().sub(p2)
    v2 = p1.copy().sub(p3)
    a = Vec3(v1.x, v1.y).cross(Vec3(v2.x, v2.y)).get_scale()

    v1 = point.copy().sub(p1)
    v2 = point.copy().sub(p2)
    a1 = Vec3(v1.x, v1.y).cross(Vec3(v2.x, v2.y)).get_scale()

    v1 = point.copy().sub(p2)
    v2 = point.copy().sub(p3)
    a2 = Vec3(v1.x, v1.y).cross(Vec3(v2.x, v2.y)).get_scale()

    v1 = point.copy().sub(p1)
    v2 = point.copy().sub(p3)
    a3 = Vec3(v1.x, v1.y).cross(Vec3(v2.x, v2.y)).get_scale()

    return a > a1 + a2 + a3 - 1e-6


vertex_buffer: list[list[Any]] = []
index_buffer: list = []
uniform_buffer: dict = {}
vertex_shader_fn = None
fragment_shader_fn = None
screen_buffer: list[int] = []
depth_buffer: list[float] = []
clear_color: Vec3 = Vec3(0, 0, 0)
screen_size: Vec2 = Vec2(640, 420)


def draw_triangles():
    if vertex_shader_fn is None or fragment_shader_fn is None:
        return

    iidxs = 0
    while iidxs < len(index_buffer):
        indices = index_buffer[iidxs : iidxs + 3]
        iidxs += 3

        vert_shader_outs: list[list[Any]] = []

        for i in indices:
            vert_shader_outs += [vertex_shader_fn(vertex_buffer[i], uniform_buffer)]

        # get positions
        vp1, vp2, vp3 = vert_shader_outs
        p1 = Vec2(
            (vp1[0].x + 1) / 2 * screen_size.x, (vp1[0].y + 1) / 2 * screen_size.y
        )
        p2 = Vec2(
            (vp2[0].x + 1) / 2 * screen_size.x, (vp2[0].y + 1) / 2 * screen_size.y
        )
        p3 = Vec2(
            (vp3[0].x + 1) / 2 * screen_size.x, (vp3[0].y + 1) / 2 * screen_size.y
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

                point = Vec2(x, y)

                # culling l3.5
                if not is_in_triangle(p1, p2, p3, point):
                    continue

                # calculating depth
                depth = triangle_lerp(
                    (p1, vp1[0].z), (p2, vp2[0].z), (p3, vp3[0].z), point
                )

                # culling l4
                if depth > depth_buffer[y * int(screen_size.x) + x]:
                    continue

                # interpolate vert_shader_outs
                lerped_vert_shader_outs = []
                for i in range(1, len(vp1)):
                    v1, v2, v3 = vp1[i], vp2[i], vp3[i]
                    lerped_vert_shader_outs += [
                        triangle_lerp_any((p1, v1), (p2, v2), (p3, v3), point)
                    ]

                color: Vec3 = fragment_shader_fn(
                    lerped_vert_shader_outs, uniform_buffer
                )
                screen_buffer[(y * int(screen_size.x) + x) * 3 + 0] = int(color.z * 255)
                screen_buffer[(y * int(screen_size.x) + x) * 3 + 1] = int(color.y * 255)
                screen_buffer[(y * int(screen_size.x) + x) * 3 + 2] = int(color.x * 255)


def upload_vertex_shader_fn(shader_fn) -> None:
    global vertex_shader_fn
    vertex_shader_fn = shader_fn


def upload_fragment_shader_fn(shader_fn) -> None:
    global fragment_shader_fn
    fragment_shader_fn = shader_fn


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


def upload_uniform(val: Any, name: str) -> None:
    global uniform_buffer
    uniform_buffer[name] = val


def save(filepath: str) -> None:
    make_bitmap(filepath, int(screen_size.x), int(screen_size.y), screen_buffer)
