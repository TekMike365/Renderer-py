import math

class Vec3():
    def __init__(self, x:float=0.0, y:float=0.0, z:float=0.0) -> None:
        self.x = x
        self.y = y
        self.z = z

    def scale(self, scalar:float):
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

    def dot(self, other) -> None:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vec3(
                self.y * other.z - self.z * other.y,
                self.z * other.x - self.x * other.z,
                self.x * other.y - self.y * other.x
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

    def rotate_x(self, rad):
        vec = Vec2(self.y, self.z).rotate(rad)
        self.y = vec.x
        self.z = vec.y
        return self

    def rotate_y(self, rad):
        vec = Vec2(self.x, self.z).rotate(rad)
        self.x = vec.x
        self.z = vec.y
        return self

    def rotate_z(self, rad):
        vec = Vec2(self.x, self.y).rotate(rad)
        self.x = vec.x
        self.y = vec.y
        return self

class Vec2():
    def __init__(self, x:float=0.0, y:float=0.0) -> None:
        self.x = x
        self.y = y

    def scale(self, scalar:float):
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
        x = cos * self.x - sin * self.y,
        y = sin * self.x + cos * self.y
        self.x = x
        self.y = y
        return self

class Mat3:
    def __init__(self, c1:Vec3=Vec3(), c2:Vec3=Vec3(), c3:Vec3=Vec3()) -> None:
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3

    def scale(self, scalar):
        self.c1.scale(scalar)
        self.c2.scale(scalar)
        self.c3.scale(scalar)
        return self

    def add(self, other):
        self.c1.add(other.c1)
        self.c2.add(other.c2)
        self.c3.add(other.c3)
        return self

    def sub(self, other):
        self.c1.sub(other.c1)
        self.c2.sub(other.c2)
        self.c3.sub(other.c3)
        return self

    def det(self) -> float:
        return self.c1.dot(self.c2.cross(self.c3))

    def transpose(self):
        r1 = Vec3(self.c1.x, self.c2.x, self.c3.x)
        r2 = Vec3(self.c1.y, self.c2.y, self.c3.y)
        r3 = Vec3(self.c1.z, self.c2.z, self.c3.z)
        self.c1 = r1
        self.c2 = r2
        self.c3 = r3
        return self

    def mult_vec(self, vec:Vec3) -> Vec3:
        return Vec3(
                self.v1.copy().scale(vec.x),
                self.v2.copy().scale(vec.y),
                self.v3.copy().scale(vec.z)
            )

    def mult(self, other):
        mat1 = self.copy().transpose()
        mat2 = other.copy()
        return Mat3(
                Vec3(
                    mat1.c1.dot(mat2.c1),
                    mat1.c2.dot(mat2.c1),
                    mat1.c3.dot(mat2.c1)
                ),
                Vec3(
                    mat1.c1.dot(mat2.c2),
                    mat1.c2.dot(mat2.c2),
                    mat1.c3.dot(mat2.c2)
                ),
                Vec3(
                    mat1.c1.dot(mat2.c3),
                    mat1.c2.dot(mat2.c3),
                    mat1.c3.dot(mat2.c3)
                )
            )

    def invert(self):
        c1 = self.c2.cross(self.c3)
        c2 = self.c3.cross(self.c1)
        c3 = self.c1.cross(self.c2)
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.scale(1 / self.det())
        return self

    def copy(self):
        return Mat3().add(self)

