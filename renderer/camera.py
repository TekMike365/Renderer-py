import math

from typing import Self
from vmath import Mat4, Vec3, Vec2


class Camera:
    def __init__(self, fov_deg: float, screen: Vec2, near: float, far: float) -> None:
        self._posmat = Mat4()
        self._near = near
        self._far = far
        self._screen = screen
        self._fov_deg = fov_deg
        self._fov_rad = 2 * math.pi * (360.0 / fov_deg)

    def change_clipping(self, near: float, far: float) -> Self:
        self._near = near
        self._far = far
        return self

    def change_fov(self, fov_deg: float) -> Self:
        self._fov_deg = fov_deg
        self._fov_rad = 2 * math.pi * (360.0 / fov_deg)
        return self

    def change_screen(self, screen: Vec2) -> Self:
        self._screen = screen
        return self

    def get_focal_len(self) -> float:
        return self._screen.x / (2 * math.atan(self._fov_rad / 2))

    def translate(self, dir: Vec3) -> Self:
        self._posmat.translate(dir.copy().scale(-1))
        return self

    def rotate(self, angle: Vec3) -> Self:
        self._posmat.rotate(angle.copy().scale(-1))
        return self

    def scale(self, scale: Vec3) -> Self:
        self._posmat.scale(scale.copy().scale(-1))
        return self
