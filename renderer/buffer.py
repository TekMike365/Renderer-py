from typing import Any


class VertexBuffer:
    def __init__(self, data: list[Any]) -> None:
        self.data = data


class IndexBuffer:
    def __init__(self, data: list[int]) -> None:
        self.data = data


class VertexArray:
    def __init__(self, vertexBuffer: VertexBuffer, indexBuffer: IndexBuffer) -> None:
        self.vertexBuffer = vertexBuffer
        self.indexBuffer = indexBuffer
