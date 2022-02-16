import pyglet
from tools.drawing import Canvas


class OrthoCanvas(Canvas):
  def __init__(self, *args, updates_per_second: int = 10, **kwargs):
    super().__init__(*args, updates_per_second=updates_per_second, **kwargs)
    self.x = 200.
    self.y = 200.
    self.z = 200.
    self.size = 100.

  def cube(self, x: float, y: float, z: float, size: float, orientation: tuple[float, float, float] = (0., 0., 0.), color: tuple[int, int, int, int] = (255, 255, 255, 100)):
    pyglet.graphics.draw(
      4, 
      pyglet.gl.GL_QUADS, 
      ("v2f", (
        x - size, y - size, 
        x - size, y + size,
        x + size, y + size,
        x + size, y - size)), 
      ("c4B", color * 4)
    )

  def _coordinates_to_screen(self, x: float, y: float, z: float) -> tuple[float, float]:
    scale = min(self.width, self.height)
    return x * scale, y * scale
    
  def _update(self, dt: float) -> None:
    ...
  
  def _on_draw(self) -> None:
    self.clear()
    self.cube(self.x, self.y, self.z, self.size, (255, 255, 255, 255))


def main():
  canvas = OrthoCanvas(width=800, height=800)
  canvas.run()


if __name__ == "__main__":
  main()
