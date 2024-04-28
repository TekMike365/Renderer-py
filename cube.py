import src.renderer as renderer

from src.vmath import Vec2, Vec3, Mat3
from src.camera import PerspectiveCam, OrthographicCam


PI = 3.141592

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

renderer.render()
renderer.save_screen("cube.bmp")

