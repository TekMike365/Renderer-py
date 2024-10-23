import math


class Vec3:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def scale(self, scalar: float):
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
    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.x = x
        self.y = y

    def scale(self, scalar: float):
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
        self, x: float = 0.0, y: float = 0.0, z: float = 0.0, w: float = 0.0
    ) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def scale(self, scalar: float):
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
