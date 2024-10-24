import math


class Vec3:
    def __init__(
        self, x: float | int = 0.0, y: float | int = 0.0, z: float | int = 0.0
    ) -> None:
        self.x = x
        self.y = y
        self.z = z

    def scale(self, scalar: float | int):
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar
        return self

    def add(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        return self

    def sub(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        return self

    def dot(self, other) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def normalize(self):
        scale = self.get_scale()
        self.x /= scale
        self.y /= scale
        self.z /= scale
        return self

    def get_scale(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def copy(self):
        return Vec3().add(self)

    def __str__(self) -> str:
        return f"[{self.x}, {self.y}, {self.z}]"


class Vec2:
    def __init__(self, x: float | int = 0.0, y: float | int = 0.0) -> None:
        self.x = x
        self.y = y

    def scale(self, scalar: float | int):
        self.x *= scalar
        self.y *= scalar
        return self

    def add(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def sub(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def dot(self, other) -> None:
        return self.x * other.x + self.y * other.y

    def normalize(self):
        scale = self.get_scale()
        self.x /= scale
        self.y /= scale
        return self

    def get_scale(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)

    def copy(self):
        return Vec2().add(self)

    def rotate(self, rad):
        cos = math.cos(rad)
        sin = math.sin(rad)
        x = cos * self.x - sin * self.y
        y = sin * self.x + cos * self.y
        self.x = x
        self.y = y
        return self

    def __str__(self) -> str:
        return f"[{self.x}, {self.y}]"


class Vec4:
    def __init__(
        self,
        x: float | int = 0.0,
        y: float | int = 0.0,
        z: float | int = 0.0,
        w: float | int = 0.0,
    ) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def scale(self, scalar: float | int):
        self.x *= scalar
        self.y *= scalar
        self.z *= scalar
        self.w *= scalar
        return self

    def add(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z
        self.w += other.w
        return self

    def sub(self, other):
        self.x -= other.x
        self.y -= other.y
        self.z -= other.z
        self.w -= other.w
        return self

    def dot(self, other) -> None:
        return self.x * other.x + self.y * other.y + self.z * other.z + self.w * other.w

    def normalize(self):
        scale = self.get_scale()
        self.x /= scale
        self.y /= scale
        self.z /= scale
        self.w /= scale
        return self

    def get_scale(self) -> float:
        return math.sqrt(self.x**2 + self.y**2 + self.z**2 + self.w**2)

    def copy(self):
        return Vec4().add(self)

    def __str__(self) -> str:
        return f"[{self.x}, {self.y}]"


class Mat4:
    def __init__(self) -> None:
        self.c1 = Vec4(1.0, 0.0, 0.0, 0.0)
        self.c2 = Vec4(0.0, 1.0, 0.0, 0.0)
        self.c3 = Vec4(0.0, 0.0, 1.0, 0.0)
        self.c4 = Vec4(0.0, 0.0, 0.0, 1.0)

    def get_scale(self) -> Vec3:
        return Vec3(self.c1.x, self.c2.y, self.c3.z)

    def get_position(self) -> Vec3:
        return Vec3(self.c4.x, self.c4.y, self.c4.z)

    def translate(self, v3: Vec3):
        self.c4.add(Vec4(v3.x, v3.y, v3.z, 0.0))
        return self

    def scale(self, v3: Vec3):
        self.c4.add(Vec4(v3.x, 0.0, 0.0))
        self.c4.add(Vec4(0.0, v3.y, 0.0, 0.0))
        self.c4.add(Vec4(0.0, 0.0, v3.z, 0.0))
        return self

    def rotate(self, angle: Vec3):
        sin = Vec3(math.sin(angle.x), math.sin(angle.y), math.sin(angle.z))
        cos = Vec3(math.cos(angle.x), math.cos(angle.y), math.cos(angle.z))

        rot_x = Mat4()
        rot_x.c2.y = cos.x
        rot_x.c2.z = sin.x
        rot_x.c3.y = -sin.x
        rot_x.c3.z = cos.x

        rot_y = Mat4()
        rot_y.c1.x = cos.x
        rot_y.c3.x = sin.x
        rot_y.c1.z = -sin.x
        rot_y.c3.z = cos.x

        rot_z = Mat4()
        rot_z.c1.y = cos.x
        rot_z.c1.z = sin.x
        rot_z.c2.y = -sin.x
        rot_z.c2.z = cos.x

        self.mul(rot_x).mul(rot_y).mul(rot_z)
        return self

    def copy(self):
        new = Mat4()
        new.c1 = self.c1
        new.c2 = self.c2
        new.c3 = self.c3
        new.c4 = self.c4
        return new

    def mul(self, other):
        result = Mat4()
        result.c1 = Vec4(
            self.c1.x * other.c1.x
            + self.c2.x * other.c1.y
            + self.c3.x * other.c1.z
            + self.c4.x * other.c1.w,
            self.c1.y * other.c1.x
            + self.c2.y * other.c1.y
            + self.c3.y * other.c1.z
            + self.c4.y * other.c1.w,
            self.c1.z * other.c1.x
            + self.c2.z * other.c1.y
            + self.c3.z * other.c1.z
            + self.c4.z * other.c1.w,
            self.c1.w * other.c1.x
            + self.c2.w * other.c1.y
            + self.c3.w * other.c1.z
            + self.c4.w * other.c1.w,
        )
        result.c1 = Vec4(
            self.c1.x * other.c2.x
            + self.c2.x * other.c2.y
            + self.c3.x * other.c2.z
            + self.c4.x * other.c2.w,
            self.c1.y * other.c2.x
            + self.c2.y * other.c2.y
            + self.c3.y * other.c2.z
            + self.c4.y * other.c2.w,
            self.c1.z * other.c2.x
            + self.c2.z * other.c2.y
            + self.c3.z * other.c2.z
            + self.c4.z * other.c2.w,
            self.c1.w * other.c2.x
            + self.c2.w * other.c2.y
            + self.c3.w * other.c2.z
            + self.c4.w * other.c2.w,
        )
        result.c1 = Vec4(
            self.c1.x * other.c3.x
            + self.c2.x * other.c3.y
            + self.c3.x * other.c3.z
            + self.c4.x * other.c3.w,
            self.c1.y * other.c3.x
            + self.c2.y * other.c3.y
            + self.c3.y * other.c3.z
            + self.c4.y * other.c3.w,
            self.c1.z * other.c3.x
            + self.c2.z * other.c3.y
            + self.c3.z * other.c3.z
            + self.c4.z * other.c3.w,
            self.c1.w * other.c3.x
            + self.c2.w * other.c3.y
            + self.c3.w * other.c3.z
            + self.c4.w * other.c3.w,
        )
        result.c1 = Vec4(
            self.c1.x * other.c4.x
            + self.c2.x * other.c4.y
            + self.c3.x * other.c4.z
            + self.c4.x * other.c4.w,
            self.c1.y * other.c4.x
            + self.c2.y * other.c4.y
            + self.c3.y * other.c4.z
            + self.c4.y * other.c4.w,
            self.c1.z * other.c4.x
            + self.c2.z * other.c4.y
            + self.c3.z * other.c4.z
            + self.c4.z * other.c4.w,
            self.c1.w * other.c4.x
            + self.c2.w * other.c4.y
            + self.c3.w * other.c4.z
            + self.c4.w * other.c4.w,
        )
        self = result
        return self
