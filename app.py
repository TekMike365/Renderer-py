import math

from vmath import Vec2, Vec3, Mat3


PI = 3.141592


class Camera:
    def __init__(self, pos:Vec3, normal:Vec3, up:Vec3, size:Vec2) -> None:
        self.pos = pos
        self.normal = normal
        self.up = up
        self.size = size

    def world_to_screen(self, point:Vec3) -> Vec2 | None:
        return None

    def _world_to_screen(self, point:Vec3, line:Vec3) -> Vec2:
        vn = self.normal.normalize()
        vy = self.up.copy()\
                    .normalize()
        vx = vy.cross(vn)\
               .normalize()
        vd = line.copy()\
                 .normalize()
        mat = Mat3(
                vd.scale(-1),
                vy,
                vx
            ).invert()
        pc = point.copy().sub(self.pos)
        vec3 = mat.transpose()\
                  .mult_vec(pc)
        vec = Vec2(-vec3.z, -vec3.y)

        # if camera is not looking
        if vec3.x > 0:
            return None

        if (vec.x < -self.size.x / 2 or
            vec.y < -self.size.y / 2 or
            vec.x > self.size.x / 2 or
            vec.y > self.size.y / 2):
            return None

        return vec

class OrthographicCam(Camera):
    def __init__(self, pos:Vec3, normal:Vec3, up:Vec3, size:Vec2) -> None:
        super().__init__(pos, normal, up, size)

    def world_to_screen(self, point:Vec3) -> Vec2 | None:
        return self._world_to_screen(point, self.normal.copy().scale(-1))

class PerspectiveCam(Camera):
    def __init__(self, pos:Vec3, normal:Vec3, up:Vec3, size:Vec2, fov_rad:float) -> None:
        super().__init__(pos, normal, up, size)
        self.fov_rad = fov_rad

    def world_to_screen(self, point:Vec3) -> Vec2 | None:
        dist = self.size.x / (2 * math.tan(self.fov_rad / 2))
        vfp = self.normal.copy()\
                         .normalize()\
                         .scale(-dist)
        fp = self.pos.copy()\
                     .add(vfp)
        line = fp.copy()\
                 .sub(point)
        return self._world_to_screen(point, line)


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

# displaying
import tkinter

root = tkinter.Tk()

RATIO = camera.size.y / camera.size.x
CW = 700
CH = CW * RATIO

canvas = tkinter.Canvas(root, width=CW, height=CH, bg="white")
canvas.pack()

for t in indices:
    i1, i2, i3 = t
    scalar = CW / camera.size.x
    offset = Vec2(CW / 2, CH / 2)
    p1 = camera.world_to_screen(vertices[i1])
    p2 = camera.world_to_screen(vertices[i2])
    p3 = camera.world_to_screen(vertices[i3])
    if p1 == None or p2 == None or p3 == None:
        continue
    p1.y *= -1
    p2.y *= -1
    p3.y *= -1
    p1 = p1.scale(scalar).add(offset)
    p2 = p2.scale(scalar).add(offset)
    p3 = p3.scale(scalar).add(offset)
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

for t in i2s:
    i1, i2 = t
    scalar = CW / camera.size.x
    offset = Vec2(CW / 2, CH / 2)
    p1 = camera.world_to_screen(vertices[i1])
    p2 = camera.world_to_screen(vertices[i2])
    if p1 == None or p2 == None:
        continue
    p1.y *= -1
    p2.y *= -1
    p1 = p1.scale(scalar).add(offset)
    p2 = p2.scale(scalar).add(offset)
    canvas.create_line(p1.x, p1.y, p2.x, p2.y, fill="tomato", width=2)

root.mainloop()

