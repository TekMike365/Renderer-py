import math

from typing import Self
from .vmath import Mat4, Vec3, Vec2


class Camera:
    def __init__(
        self, fov_deg: float, screen_size: Vec2, near: float, far: float
    ) -> None:
        self._posmat = Mat4()
        self._near = near
        self._far = far
        self._screen_size = screen_size
        self._fov_deg = fov_deg
        self._fov_rad = 2 * math.pi * (360.0 / fov_deg)
        self._focal_len = self._screen_size.x / (2 * math.atan(self._fov_rad / 2))

    def change_clipping(self, near: float, far: float) -> Self:
        self._near = near
        self._far = far
        return self

    def change_fov(self, fov_deg: float) -> Self:
        self._fov_deg = fov_deg
        self._fov_rad = 2 * math.pi * (360.0 / fov_deg)
        self._focal_len = self._screen_size.x / (2 * math.atan(self._fov_rad / 2))
        return self

    def change_screen(self, screen: Vec2) -> Self:
        self._screen_size = screen
        return self

    def translate(self, dir: Vec3) -> Self:
        self._posmat.translate(dir.copy().scale(-1))
        return self

    def rotate(self, angle: Vec3) -> Self:
        self._posmat.rotate(angle.copy().scale(-1))
        return self

    def scale(self, scale: Vec3) -> Self:
        self._posmat.scale(scale.copy().scale(-1))
        return self

    def world2screen_pos(self, point: Vec3) -> Vec3:
        t = self._focal_len / (self._focal_len - point.z)
        return Vec3(
            point.x * t / self._screen_size.x, point.y * t / self._screen_size.y, t
        )
