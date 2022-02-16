import pyglet
from typing import Collection
import math


def concentration(values: Collection[float]) -> float:
  '''
  Given a collection of values, return the concentration of the values. 
  
  The concentration of a collection of values is the proportion of the values that are the maximum
  value of the collection.
  
  :param values: Collection[float]
  :type values: Collection[float]
  :return: The concentration of the values.
  '''
  assert all(x >= 0. for x in values)
  no_values = len(values)
  if 0 >= no_values:
      return 0.
  if 1 >= no_values:
    return 1.

  value_sum = sum(values)
  if 1 >= no_values:
      return float(0. < value_sum)

  value_average = value_sum / no_values
  normalize_quotient = value_sum - value_average
  if 0. >= normalize_quotient:
    return 0.

  return (max(values) - value_average) / normalize_quotient


def g(x: int) -> float:
  '''
  Given a positive integer, return the probability that a random variable will have a value less than
  or equal to the input
  
  :param x: The number of times the function has been called
  :type x: int
  :return: 1 / 2 ** math.ceil(math.log(x + 1, 2))
  '''
  assert not (x < 0)
  if x == 0:
    return 0.
  return 1 / 2 ** math.ceil(math.log(x + 1, 2))


def h(x: int) -> int:
  '''
  Given a positive integer, return the number of 1's in the binary representation of that number
  
  :param x: The number of bits in the binary representation of the number
  :type x: int
  :return: The number of bits needed to represent the number x.
  '''
  assert not (x < 0)
  if x == 0:
    return 0
  return 2 ** math.ceil(math.log(x + 1, 2)) - x - 1


def spreadIterative(x: int) -> float:
  """
  Maximizes the circumference distance between successive non-negative integers while minimizing total concentration on a circle.

  :param x: Input integer index.
  :return: Float from [0., 1.] indicating position on circumference of circle.
  """
  assert not (x < 0)
  if x == 0:
    return 0.
  s = 0.
  while x > 0:
    s += g(x)
    x = h(x - 1)
  return s


def linear_to_circular(x: float, y: float, value: float, radius: float=1.) -> tuple[float, float]:
  '''
  Given a value between 0 and 1, return the corresponding point on a circle of radius 1
  
  :param x: The x coordinate of the center of the circle
  :type x: float
  :param y: The y-coordinate of the center of the circle
  :type y: float
  :param value: the value of the parameter, between 0 and 1
  :type value: float
  :param radius: The radius of the circle
  :type radius: float
  :return: The coordinates of the point on the circle.
  '''
  assert 1. >= value >= 0.
  assert 0. < radius
  theta = 2. * math.pi * value
  return x + radius * math.cos(theta), y + radius * math.sin(theta)


class Canvas(pyglet.window.Window):
  def __init__(self, *args, interval=.1, **kwargs):
    super().__init__(*args, **kwargs)
    self.iteration = 0
    self.this_circle = -1.
    self.last_circle = -1.

    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

    pyglet.clock.schedule_interval(self.update, interval)
      
  @staticmethod
  def circle(x: float, y: float, r: float):
    '''
    Draw a circle with center at (x, y) and radius r
    
    :param x: the x coordinate of the center of the circle
    :type x: float
    :param y: the y coordinate of the center of the circle
    :type y: float
    :param r: radius of the circle
    :type r: float
    '''
    no_segments = 64

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
        ("c4B", (255, 255, 255, 255,
                 255, 255, 255, 255))
        )

  def clear(self) -> None:
    '''
    Clear the screen by drawing a black rectangle over the entire screen
    '''
    pyglet.graphics.draw(
      4, 
      pyglet.gl.GL_QUADS, 
      ("v2f", (0, 0, 0, self.height, self.width, self.height, self.width, 0)), 
      ("c4B", (0, 0, 0, 10,
               0, 0, 0, 10,
               0, 0, 0, 10,
               0, 0, 0, 10))
      )

  def update(self, dt: float) -> None:
    '''
    The function iterates through the list of circles and updates their positions
    
    :param dt: The time in seconds since the last update
    :type dt: float
    '''
    if self.has_exit:
      pyglet.app.exit()

    self.last_circle = self.this_circle
    # self.this_circle = spreadIterative(self.iteration)
    self.this_circle = (max(0., self.this_circle) + .001) % 1.

    self.iteration += 1

  def on_draw(self) -> None:
    '''
    Draw a circle at the last point of the spiral, and draw a line from that point to the next point
    of the spiral
    '''
    x_mid = self.width // 2
    y_mid = self.height // 2

    r = min(x_mid, y_mid)

    self.clear()
    if self.last_circle >= 0.:
      from_x, from_y = linear_to_circular(0., 0., self.last_circle, radius=r * .8)
      to_x, to_y = linear_to_circular(0., 0., self.this_circle, radius=r * .8)
      Canvas.circle(x_mid + to_x, y_mid + to_y, 10.)
      pyglet.graphics.draw(
        2, pyglet.gl.GL_LINES, 
        ("v2f", (from_x + x_mid, from_y + y_mid, to_x + x_mid, to_y + y_mid)),
        ("c4B", (255, 255, 255, 128,
                 255, 255, 255, 128))
        )


def main():
  config = pyglet.gl.Config(sample_buffers=1, samples=4)
  canvas = Canvas(config=config, width=1024, height=768, interval=.01)
  
  pyglet.app.run()


if __name__ == '__main__':
  main()
