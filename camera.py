from math import tan
from vmath import Vec2, Vec3, Mat3

class Camera:
    def __init__(self, pos:Vec3, normal:Vec3, up:Vec3, size:Vec2) -> None:
        self.pos = pos
        self.normal = normal
        self.up = up
        self.size = size

    def world_to_screen(self, point:Vec3) -> Vec2 | None:
        return None

    def is_visible(self, screen_point:Vec3) -> bool:
        # if camera is not looking
        if screen_point.x < 0:
            return False

        if (screen_point.x < -self.size.x / 2 or
            screen_point.y < -self.size.y / 2 or
            screen_point.x > self.size.x / 2 or
            screen_point.y > self.size.y / 2):
            return False

        return True

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
        return Vec3(-vec3.z, -vec3.y, -vec3.z)

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
        dist = self.size.x / (2 * tan(self.fov_rad / 2))
        vfp = self.normal.copy()\
                         .normalize()\
                         .scale(-dist)
        fp = self.pos.copy()\
                     .add(vfp)
        line = fp.copy()\
                 .sub(point)
        return self._world_to_screen(point, line)

