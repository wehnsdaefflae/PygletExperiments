import math
import pyglet


class Canvas(pyglet.window.Window):
  def __init__(self, *args, updates_per_second: int = 10, **kwargs):
    super().__init__(*args, config=pyglet.gl.Config(sample_buffers=1, samples=4), **kwargs)
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

    if updates_per_second >= 1:
      pyglet.clock.schedule_interval(self.update, 1. / updates_per_second)
      
  @staticmethod
  def circle(x: float, y: float, r: float, color: tuple[int, int, int, int], no_segments: int = 64):
    '''
    Draw a circle with center at (x, y) and radius r
    
    :param x: the x coordinate of the center of the circle
    :type x: float
    :param y: the y coordinate of the center of the circle
    :type y: float
    :param r: radius of the circle
    :type r: float
    :param no_segments: the number of segments used to draw the circle, defaults to 64
    :type no_segments: int (optional)
    '''
    for i in range(no_segments):
      theta1 = 2 * math.pi * i / no_segments
      theta2 = 2 * math.pi * (i + 1) / no_segments
      x1 = x + r * math.cos(theta1)
      y1 = y + r * math.sin(theta1)
      x2 = x + r * math.cos(theta2)
      y2 = y + r * math.sin(theta2)
      pyglet.graphics.draw(
        2, 
        pyglet.gl.GL_LINES, 
        ("v2f", (x1, y1, x2, y2)),
        ("c4B", color + color)
        )

  def update(self, dt: float) -> None:
    if self.has_exit:
      pyglet.app.exit()
      
    self._update(dt)
  
  def on_draw(self) -> None:
    self._on_draw()

  def _update(self, dt: float) -> None:
    '''
    Update the canvas content.
    
    The `update` function is called once per frame. This is where you define the logic.
    
    :param dt: float
    :type dt: float
    '''
    raise NotImplementedError()

  def _on_draw(self) -> None:
    '''
    The `on_draw` function is called every time the window is supposed to be drawn.
    '''
    raise NotImplementedError()
