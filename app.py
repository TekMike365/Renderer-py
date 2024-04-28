import math

from vmath import Vec2, Vec3, Mat3
from camera import PerspectiveCam, OrthographicCam
from bitmap import make_bitmap


PI = 3.141592


vertices = [
    Vec3(-0.5, -0.5, -0.5),
    Vec3( 0.5, -0.5, -0.5),
    Vec3( 0.5, -0.5,  0.5),
    Vec3(-0.5, -0.5,  0.5),

    Vec3(-0.5,  0.5, -0.5),
    Vec3( 0.5,  0.5, -0.5),
    Vec3( 0.5,  0.5,  0.5),
    Vec3(-0.5,  0.5,  0.5)
]

indices = [
    (2, 3, 0),
    (0, 1, 2),

    (1, 0, 4),
    (4, 5, 1),

    (2, 1, 5),
    (5, 6, 2),

    (0, 3, 7),
    (7, 4, 0),

    (3, 2, 6),
    (6, 7, 3),

    (5, 4, 7),
    (7, 6, 5)
]

#indices = [
#    (1, 0, 4),
#    (3, 2, 6)
#]

# scale, rotate, move
for vertex in vertices:
    vertex.scale(5.0)
    vertex.rotate_x(PI * 0.0)\
          .rotate_y(PI * 0.0)\
          .rotate_z(PI * 0.0)
    vertex.add(Vec3(3.0, 0.0, 0.0))

pos = Vec3(z=-10.0)
normal = Vec3(z=1.0)
up = Vec3(y=1.0)
size = Vec2(6.4, 4.8)
fov_rad = 60 * PI / 180 
#camera = OrthographicCam(pos, normal, up, size)
camera = PerspectiveCam(pos, normal, up, size, fov_rad)



RATIO = camera.size.y / camera.size.x
CW = 640
CH = int(CW * RATIO)
SCALAR = CW / camera.size.x
OFFSET = Vec3(CW / 2, CH / 2, 0.0)

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
    return v1 + t * (v2 - v1)

def triangle_lerp(vt:Vec2, v1:Vec3, v2:Vec3, v3:Vec3) -> float | None:
    va = Vec2(v2.x, v2.y).sub(Vec2(v1.x, v1.y))
    vc = vt.copy().sub(Vec2(v3.x, v3.y))

    b = vc.y * (v1.x - v3.x) - vc.x * (v1.y - v3.y)
    a = vc.y * va.x - vc.x * va.y

    if a == 0:
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        return None

    t = - b / a

    vi = Vec2(v1.x, v1.y).add(va.copy().scale(t))
    i = lerp(v1.z, v2.z, t)

    vn = Vec2(v3.x, v3.y).sub(vi)

    if vn.get_scale() == 0:
        print("aaaaaaaaaaaaaaaaaaaaaaa")
        return None
    
    s = vc.get_scale() / vn.get_scale()

    return lerp(v3.z, i, s)

# rasterizing
# pixel = (depth, r, g, b)
# triangle = (pos, size, pixel_array)
triangles = []
for t in indices:
    i1, i2, i3 = t
    v1 = camera.world_to_screen(vertices[i1])
    v2 = camera.world_to_screen(vertices[i2])
    v3 = camera.world_to_screen(vertices[i3])

    if not camera.is_visible(v1) and not camera.is_visible(v2) and not camera.is_visible(v3):
        continue
    
    p1 = v1.copy().scale(SCALAR).add(OFFSET)
    p2 = v2.copy().scale(SCALAR).add(OFFSET)
    p3 = v3.copy().scale(SCALAR).add(OFFSET)
    p1 = vec3_to_vec3i(p1)
    p2 = vec3_to_vec3i(p2)
    p3 = vec3_to_vec3i(p3)

    # get outline box
    pos = Vec2(
        min(p1.x, p2.x, p3.x),
        min(p1.y, p2.y, p3.y)
    )
    size = Vec2(
        max(p1.x, p2.x, p3.x),
        max(p1.y, p2.y, p3.y)
    ).sub(pos)

    # coloring
    # pixel = (depth, r, g, b)
    pixel_array = []
    for x in range(size.y):
        for y in range(size.x):
            p = Vec2(x, y).add(pos)

            area = get_triangle_area(Vec2(p1.x, p1.y), Vec2(p2.x, p2.y), Vec2(p3.x, p3.y))
            area_1 = get_triangle_area(p, Vec2(p2.x, p2.y), Vec2(p3.x, p3.y))
            area_2 = get_triangle_area(Vec2(p1.x, p1.y), p, Vec2(p3.x, p3.y))
            area_3 = get_triangle_area(Vec2(p1.x, p1.y), Vec2(p2.x, p2.y), p)
            
            s = area_1 + area_2 + area_3 - area
            tolerance = 100
            inside = s <= tolerance and s >= -tolerance
            outline = (area_1 < tolerance or
                       area_2 < tolerance or
                       area_3 < tolerance) and inside

            depth = -1
            red   = 0xff
            green = 0xff
            blue  = 0xff

            
            if inside:
                depth = triangle_lerp(p, p1, p2, p3)
                if depth == None:
                    depth = 1000
                red   = 0xff
                green = 0xff
                blue  = 0x00
            if outline:
                red   = 0x00
                green = 0x00
                blue  = 0x00

            pixel_array.append((depth, red, green, blue))

    #print(size, len(pixel_array))
    #print(pos)
    #print(pos.copy().add(size))
    #print(p1)
    #print(p2)
    #print(p3)
    triangles.append((pos, size, pixel_array))

# bgr
pixel_data = [ 0xff, 0xff, 0x00 ] * CW * CH
pixel_depths = [ -1 ] * CW * CH 
for t in triangles:
    pos, size, pixel_array = t

    for m in range(size.y):
        for n in range(size.x):
            x = pos.x + n 
            y = pos.y + m
            i = CW * y + x
            j = i * 3
            k = size.x * m + n

            old_d = pixel_depths[i]
            d, r, g, b = pixel_array[k]

            if d == -1:
                continue

            if (old_d == -1 or d < old_d):
                pixel_depths[i] = d
                pixel_data[j + 0] = b
                pixel_data[j + 1] = g
                pixel_data[j + 2] = r

make_bitmap("scene.bmp", CW, CH, pixel_data)


# displaying wireframe
import tkinter

root = tkinter.Tk()

canvas = tkinter.Canvas(root, width=CW, height=CH, bg="white")
canvas.pack()

for t in indices:
    i1, i2, i3 = t
    p1 = camera.world_to_screen(vertices[i1])
    p2 = camera.world_to_screen(vertices[i2])
    p3 = camera.world_to_screen(vertices[i3])
    if p1 == None or p2 == None or p3 == None:
        continue
    p1.y *= -1
    p2.y *= -1
    p3.y *= -1
    p1 = p1.scale(SCALAR).add(OFFSET)
    p2 = p2.scale(SCALAR).add(OFFSET)
    p3 = p3.scale(SCALAR).add(OFFSET)
    canvas.create_line(p1.x, p1.y, p2.x, p2.y)
    canvas.create_line(p2.x, p2.y, p3.x, p3.y)
    canvas.create_line(p3.x, p3.y, p1.x, p1.y)

# outline
i2s = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),

    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7),

    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4)
]

#for t in i2s:
#    i1, i2 = t
#    p1 = camera.world_to_screen(vertices[i1])
#    p2 = camera.world_to_screen(vertices[i2])
#    if p1 == None or p2 == None:
#        continue
#    p1.y *= -1
#    p2.y *= -1
#    p1 = p1.scale(SCALAR).add(OFFSET)
#    p2 = p2.scale(SCALAR).add(OFFSET)
#    canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill="tomato", width=2)

root.mainloop()

