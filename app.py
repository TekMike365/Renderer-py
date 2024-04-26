from vmath import Vec2, Vec3, Mat3

class Camera:
    def __init__(self, pos:Vec3, normal:Vec3, size:Vec2) -> None:
        self.pos = pos
        self.normal = normal
        self.size = size

    def world_to_screen(self, point:Vec3) -> Vec2 | None:
        return None

    def _world_to_screen(self, point:Vec3, line:Vec3) -> Vec2:
        # temporary
        vx = Vec3(x=1.0)
        vy = Vec3(y=1.0)
        #vn = Vec3(z=1.0)
        mat = Mat3(
                line.copy().scale(-1),
                vx,
                vy
            ).invert()
        vec3 = mat.mult_vec(point.copy().sub(self.pos))
        vec = Vec2(vec3.y, vec3.z)

        if (vec.x >= -self.size.x and
            vec.y >= -self.size.y and
            vec.x <= self.size.x and
            vec.y <= self.size.y):
            return vec
        return None

class OrthographicCam(Camera):
    def __init__(self, pos:Vec3, normal:Vec3, size:Vec2) -> None:
        super().__init__(pos, normal, size)

    def world_to_screen(self, point:Vec3) -> Vec2 | None:
        return self._world_to_screen(point, self.normal)

class PerspectiveCam(Camera):
    def __init__(self, pos:Vec3, normal:Vec3, size:Vec2, fov_rad:float) -> None:
        super().__init__(pos, normal, size)
        self.fov_rad = fov_rad

    def world_to_screen(self, point:Vec3) -> Vec2 | None:
        #return self._world_to_screen(point)
        return None


vertices = [
    Vec3(-0.5, -0.5, -0.5),
    Vec3( 0.5, -0.5, -0.5),
    Vec3( 0.5,  0.5, -0.5),
    Vec3(-0.5,  0.5, -0.5),

    Vec3(-0.5, -0.5,  0.5),
    Vec3( 0.5, -0.5,  0.5),
    Vec3( 0.5,  0.5,  0.5),
    Vec3(-0.5,  0.5,  0.5)
]

import math
# rotate vertices
for vertex in vertices:
    a1 = math.radians(30)
    a2 = math.radians(30)
    vertex.rotate_y(a1).rotate_x(a1)


indices = [
    (0, 1, 2),
    (0, 2, 3),

    (0, 1, 5),
    (0, 5, 4),

    (1, 2, 6),
    (1, 6, 5),

    (3, 0, 4),
    (3, 4, 7),

    (2, 3, 7),
    (2, 7, 6),

    (4, 5, 6),
    (4, 6, 7)
]


CH = 480
CW = 640
RATIO = CH / CW

pos = Vec3(z=-2.0)
normal = Vec3(z=1.0)
size = Vec2(4.0, 4.0 * RATIO)
camera = OrthographicCam(pos, normal, size)

points = []
for vertex in vertices:
    point = camera.world_to_screen(vertex)
    if point == None:
        points.append(Vec2())
        continue
    points.append(point)



import tkinter

root = tkinter.Tk()

canvas = tkinter.Canvas(root, width=CW, height=CH)
canvas.pack()

for t in indices:
    i1, i2, i3 = t
    scalar = CW / camera.size.x
    offset = Vec2(CW, CH / 2)
    p1 = points[i1].copy().scale(scalar).add(offset)
    p2 = points[i2].copy().scale(scalar).add(offset)
    p3 = points[i3].copy().scale(scalar).add(offset)
    canvas.create_line(p1.x, p1.y, p2.x, p2.y)
    canvas.create_line(p2.x, p2.y, p3.x, p3.y)
    canvas.create_line(p3.x, p3.y, p1.x, p1.y)

root.mainloop()

