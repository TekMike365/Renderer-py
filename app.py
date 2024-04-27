from vmath import Vec2, Vec3, Mat3

class Camera:
    def __init__(self, pos:Vec3, normal:Vec3, up:Vec3, size:Vec2) -> None:
        self.pos = pos
        self.normal = normal
        self.up = up
        self.size = size

    def world_to_screen(self, point:Vec3) -> Vec2 | None:
        return None

    def _world_to_screen(self, point:Vec3, line:Vec3) -> Vec2:
        vn = self.normal
        vy = self.up.copy().scale(-1)
        vx = vy.cross(vn)
        mat = Mat3(
                line,
                vy,
                vx
            ).invert()
        vec3 = mat.mult_vec(point.copy().sub(self.pos))
        vec = Vec2(vec3.z, vec3.y)

        # if camera is not looking
        if vec3.x < 0:
            return None

        if (vec.x < -self.size.x or
            vec.y < -self.size.y or
            vec.x > self.size.x or
            vec.y > self.size.y):
            return None
        return vec

class OrthographicCam(Camera):
    def __init__(self, pos:Vec3, normal:Vec3, up:Vec3, size:Vec2) -> None:
        super().__init__(pos, normal, up, size)

    def world_to_screen(self, point:Vec3) -> Vec2 | None:
        return self._world_to_screen(point, self.normal)

class PerspectiveCam(Camera):
    def __init__(self, pos:Vec3, normal:Vec3, up:Vec3, size:Vec2, fov_rad:float) -> None:
        super().__init__(pos, normal, up, size)
        self.fov_rad = fov_rad

    def world_to_screen(self, point:Vec3) -> Vec2 | None:
        #return self._world_to_screen(point)
        return None


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


for vertex in vertices:
    PI = 3.141592
    vertex.rotate_x(PI * 0.25)\
          .rotate_y(PI * 0.25)\
          .rotate_z(PI * 0)

CH = 480
CW = 640
RATIO = CH / CW

pos = Vec3(z=-10.0)
normal = Vec3(z=1.0)
up = Vec3(y=1.0)
size = Vec2(4.0, 4.0 * RATIO)
camera = OrthographicCam(pos, normal, up, size)


import tkinter

root = tkinter.Tk()

canvas = tkinter.Canvas(root, width=CW, height=CH)
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
    p1 = p1.scale(scalar).add(offset)
    p2 = p2.scale(scalar).add(offset)
    p3 = p3.scale(scalar).add(offset)
    canvas.create_line(p1.x, p1.y, p2.x, p2.y)
    canvas.create_line(p2.x, p2.y, p3.x, p3.y)
    canvas.create_line(p3.x, p3.y, p1.x, p1.y)

root.mainloop()

