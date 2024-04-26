from vmath import Vec2, Vec3, Mat3

class Camera:
    def __init__(self) -> None:
        # params: plane, size
        pass

    def world_to_screen(self, vec3:Vec3) -> Vec2 | None:
        return None

    def _world_to_screen(self) -> Vec2:
        pass

class OrthoCam(Camera):
    def __init__(self) -> None:
        pass

    def world_to_screen(self, vec3:Vec3) -> Vec2 | None:
        return None

class PerspectiveCam(Camera):
    def __init__(self) -> None:
        pass

    def world_to_screen(self, vec3:Vec3) -> Vec2 | None:
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

