from copy import deepcopy

from .vmath import Vec2, Vec3, Mat3
from .camera import PerspectiveCam, OrthographicCam, Camera
from .bitmap import make_bitmap


# global variables
vertices:list[list]      = []  # first elemnt in nested list must be position
indices:list[tuple[int]] = []  # each tuple must have three indices
camera:Camera = None
screen_width  = 400
screen_height = 400
back_fill:tuple[int] = (0x00, 0x00, 0x00)  # RGB (max 255)
# pixel = (depth:float, red:int, green:int, blue:int)
_screen:list[tuple[float | int]] = []  # list of pixels


def get_triangle_area(p1:Vec2, p2:Vec2, p3:Vec2) -> float:
    v1 = p1.copy().sub(p3)
    v2 = p2.copy().sub(p3)
    return Vec3(v1.x, v1.y, 0.0).cross(Vec3(v2.x, v2.y, 0.0)).get_scale() / 2

def vec3_to_vec3i(vec:Vec3) -> Vec3:
    return Vec3(
            int(vec.x),
            int(vec.y),
            int(vec.z)
        )

def lerp(v1:float, v2:float, t:float) -> float:
    return (1 - t) * v1 + t * v2

def tlerp(v1:float, v2:float, v3:float, t:float, s:float) -> float:
    i = lerp(v1, v2, t)
    return lerp(v3, i, s)

def triangle_lerp(vt:Vec2, v1:Vec3, v2:Vec3, v3:Vec3) -> float | None:
    va = Vec2(v2.x, v2.y).sub(Vec2(v1.x, v1.y))
    vc = vt.copy().sub(Vec2(v3.x, v3.y))

    b = vc.y * (v1.x - v3.x) - vc.x * (v1.y - v3.y)
    a = vc.y * va.x - vc.x * va.y

    if a == 0:
        return None

    t = - b / a

    vi = Vec2(v1.x, v1.y).add(va.copy().scale(t))
    i = lerp(v1.z, v2.z, t)

    vn = vi.copy().sub(Vec2(v3.x, v3.y))

    if vn.get_scale() == 0:
        return None
    
    s = vc.get_scale() / vn.get_scale()

    return lerp(v3.z, i, s)

def get_triangle_lerp(vt:Vec2, v1:Vec3, v2:Vec3, v3:Vec3) -> tuple[float] | None:
    va = Vec2(v2.x, v2.y).sub(Vec2(v1.x, v1.y))
    vc = vt.copy().sub(Vec2(v3.x, v3.y))

    b = vc.y * (v1.x - v3.x) - vc.x * (v1.y - v3.y)
    a = vc.y * va.x - vc.x * va.y

    if a == 0:
        return None

    t = - b / a

    vi = Vec2(v1.x, v1.y).add(va.copy().scale(t))

    vn = vi.copy().sub(Vec2(v3.x, v3.y))

    if vn.get_scale() == 0:
        return None
    
    s = vc.get_scale() / vn.get_scale()

    return (t, s)

def init() -> None:
    global _screen, back_fill, screen_width, screen_height
    r, g, b = back_fill
    _screen = [ (-1, r, g, b) ] * screen_width * screen_height

""" vertex_shader
    :params: vertex data with position
    :returns: a buffer for index shader
"""
def vertex_shader(vertex:list) -> list:
    return []

""" fragment_shader
    :params: buffer:list (first element is always position)
    :returns: a tuple of RGB colors (max 255)
"""
def fragment_shader(buffer:list) -> tuple[int]:
    return (0x00, 0x00, 0x00)

def save_screen(file_path:str) -> None:
    global _screen, screen_width, screen_height
    pixel_data = []
    for pixel in _screen:
        _, r, g, b = pixel
        pixel_data.extend([b, g, r])
    make_bitmap(file_path, screen_width, screen_height, pixel_data)

def _clamp(v:float|int, a:float|int, b:float|int) -> float|int:
    if v < a:
        return a
    if v > b:
        return b
    return v

def render() -> None:
    global _screen, screen_width, screen_height, camera, vertices, indices
    SCALAR = screen_width / camera.size.x
    OFFSET = Vec3(screen_width / 2, screen_height / 2, 0.0)

    for t in indices:
        i1, i2, i3 = t
        triangle = [
            deepcopy(vertices[i1]),
            deepcopy(vertices[i2]),
            deepcopy(vertices[i3])
        ]

        is_visible = False
        for vertex in triangle:
            vertex[0] = camera.world_to_screen(vertex[0])
            if not is_visible:
                is_visible = camera.is_visible(vertex[0])

        if not is_visible:
            continue

        buffers = []
        for vertex in triangle:
            vertex[0] = vertex[0].scale(SCALAR)\
                                 .add(OFFSET)
            vertex[0] = vec3_to_vec3i(vertex[0])

            buffer = vertex_shader(vertex)
            buffers.append(buffer)

        pos = Vec2(
            min(triangle[0][0].x, triangle[1][0].x, triangle[2][0].x),
            min(triangle[0][0].y, triangle[1][0].y, triangle[2][0].y)
        )
        size = Vec2(
            max(triangle[0][0].x, triangle[1][0].x, triangle[2][0].x),
            max(triangle[0][0].y, triangle[1][0].y, triangle[2][0].y)
        ).sub(pos)

        if pos.x < 0:
            pos.x = 0
        if pos.y < 0:
            pos.y = 0
        if pos.x + size.x > screen_width:
            size.x = screen_width - pos.x
        if pos.y + size.y > screen_height:
            size.y = screen_height - pos.y

        for m in range(size.y):
            for n in range(size.x):
                x = pos.x + n
                y = pos.y + m

                v  = Vec2(x, y)
                v1 = Vec2(triangle[0][0].x, triangle[0][0].y)
                v2 = Vec2(triangle[1][0].x, triangle[1][0].y)
                v3 = Vec2(triangle[2][0].x, triangle[2][0].y)

                a  = get_triangle_area(v1, v2, v3)
                a1 = get_triangle_area( v, v2, v3)
                a2 = get_triangle_area(v1,  v, v3)
                a3 = get_triangle_area(v1, v2, v)

                tolerance = 1
                d = a1 + a2 + a3 - a
                is_inside = d <= tolerance and d >= -tolerance

                if not is_inside:
                    continue

                ts = get_triangle_lerp(v, v1, v2, v3)
                if ts == None:
                    continue
                t, s = ts

                depth = tlerp(
                    triangle[0][0].z,
                    triangle[1][0].z,
                    triangle[2][0].z,
                    t, s
                )

                d, _, _, _ = _screen[screen_width * y + x]
                if depth > d and d != -1:
                    continue

                buffer = [
                    Vec3(x, y, depth)
                ]

                for i in range(len(buffers[0])):
                    e1 = buffers[0][i]
                    e2 = buffers[1][i]
                    e3 = buffers[2][i]

                    e = None

                    if isinstance(e1, float):
                        e = tlerp(e1, e2, e3, t, s)
                    elif isinstance(e1, int):
                        e = int(tlerp(e1, e2, e3, t, s))
                    elif isinstance(e1, Vec2):
                        e = Vec2(
                            tlerp(e1.x, e2.x, e3.x, t, s),
                            tlerp(e1.y, e2.y, e3.y, t, s)
                        )
                    elif isinstance(e1, Vec3):
                        e = Vec3(
                            tlerp(e1.x, e2.x, e3.x, t, s),
                            tlerp(e1.y, e2.y, e3.y, t, s),
                            tlerp(e1.z, e2.z, e3.z, t, s)
                        )

                    if e == None:
                        continue

                    buffer.append(e)

                r, g, b = fragment_shader(buffer)

                r = _clamp(r, 0, 255)
                g = _clamp(g, 0, 255)
                b = _clamp(b, 0, 255)

                _screen[screen_width * y + x] = (depth, r, g, b)

