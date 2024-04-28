import src.renderer as renderer

from copy import deepcopy

from src.vmath import Vec2, Vec3, Mat3
from src.camera import PerspectiveCam, OrthographicCam


PI = 3.141592
PREVIEW = True
OUT_FILE_PATH = "cube.bmp"

VERTICES = [
    [ Vec3(-0.5, -0.5, -0.5), Vec3(1.0, 0.0, 0.0) ],
    [ Vec3( 0.5, -0.5, -0.5), Vec3(0.0, 1.0, 0.0) ],
    [ Vec3( 0.5, -0.5,  0.5), Vec3(0.0, 1.0, 0.0) ],
    [ Vec3(-0.5, -0.5,  0.5), Vec3(1.0, 0.0, 0.0) ],

    [ Vec3(-0.5,  0.5, -0.5), Vec3(0.0, 0.0, 1.0) ],
    [ Vec3( 0.5,  0.5, -0.5), Vec3(1.0, 1.0, 1.0) ],
    [ Vec3( 0.5,  0.5,  0.5), Vec3(1.0, 1.0, 1.0) ],
    [ Vec3(-0.5,  0.5,  0.5), Vec3(0.0, 0.0, 1.0) ]
]

INDICES = [
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


# scale, rotate, move
for vertex in VERTICES:
    pos = vertex[0]
    pos.scale(5.0)
    pos.rotate_x(PI * 0.2)\
       .rotate_y(PI * 0.2)\
       .rotate_z(PI * 0.2)
    pos.add(Vec3(0.0, 0.0, 0.0))

# camera setup
pos = Vec3(z=-10.0)
normal = Vec3(z=1.0)
up = Vec3(y=1.0)
size = Vec2(6.4, 4.8)
fov_rad = 60 * PI / 180 
#camera = OrthographicCam(pos, normal, up, size)
camera = PerspectiveCam(pos, normal, up, size, fov_rad)


# screen setup
RATIO = camera.size.y / camera.size.x
CW = 640
CH = int(CW * RATIO)

# rendering
renderer.camera = camera
renderer.screen_width = CW
renderer.screen_height = CH
renderer.back_fill = (0x00, 0xff, 0xff)
renderer.indices = INDICES
renderer.vertices = VERTICES
renderer.init()

def vertex_shader(vertex:list) -> list:
    return [vertex[1]]

def fragment_shader(buffer:list) -> tuple[int]:
    color = buffer[1]
    t = (
        int(255 * color.x),
        int(255 * color.y),
        int(255 * color.z)
    )
    return t

renderer.vertex_shader = vertex_shader
renderer.fragment_shader = fragment_shader


if PREVIEW:
    import tkinter

    root = tkinter.Tk()

    canvas = tkinter.Canvas(root, width=CW, height=CH, bg="white")
    canvas.pack()

    SCALAR = CW / camera.size.x
    OFFSET = Vec3(CW / 2, CH / 2, 0.0)

    for t in INDICES:
        i1, i2, i3 = t
        triangle = [
            deepcopy(VERTICES[i1]),
            deepcopy(VERTICES[i2]),
            deepcopy(VERTICES[i3])
        ]

        is_visible = False
        for vertex in triangle:
            vertex[0] = camera.world_to_screen(vertex[0])
            if not is_visible:
                is_visible = camera.is_visible(vertex[0])

        if not is_visible:
            continue

        for vertex in triangle:
            vertex[0] = vertex[0].scale(SCALAR)\
                                 .add(OFFSET)

        p1 = Vec2(triangle[0][0].x, triangle[0][0].y)
        p2 = Vec2(triangle[1][0].x, triangle[1][0].y)
        p3 = Vec2(triangle[2][0].x, triangle[2][0].y)
        canvas.create_line(p1.x, p1.y, p2.x, p2.y)
        canvas.create_line(p2.x, p2.y, p3.x, p3.y)
        canvas.create_line(p3.x, p3.y, p1.x, p1.y)

    root.mainloop()
else:
    renderer.render()
    renderer.save_screen(OUT_FILE_PATH)

