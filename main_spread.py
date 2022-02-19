# coding=utf-8
from tools.spread import spread_iterative
from tools.various import linear_to_circular, uniformity_on_circumference
from tools.drawing import Canvas

import pyglet


class SpreadCanvas(Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.iteration = 0
        self.distance = -1.

        self.average_distance = -1.
        self.uniformity = -1.

        self.this_circle = 0.
        self.last_circle = -1.

        self.mouse_released = False

        self.points = []

        self._main_circle()

    def fade(self) -> None:
        pyglet.graphics.draw(
            4,
            pyglet.gl.GL_QUADS,
            ("v2f", (0, 20, 0, self.height, self.width, self.height, self.width, 20)),
            ("c4B", (0, 0, 0, 10,
                     0, 0, 0, 10,
                     0, 0, 0, 10,
                     0, 0, 0, 10))
        )
        pyglet.graphics.draw(
            4,
            pyglet.gl.GL_QUADS,
            ("v2f", (0, 0, 0, 20, self.width, 20, self.width, 0)),
            ("c4B", (0, 0, 0, 255,
                     0, 0, 0, 255,
                     0, 0, 0, 255,
                     0, 0, 0, 255))
        )

    def _update(self, dt: float) -> None:
        if False and not self.mouse_released:
            return

        self.mouse_released = False

        self.last_circle = self.this_circle
        self.this_circle = spread_iterative(self.iteration)
        # self.this_circle = (self.this_circle + .4) % 1.

        self.points.append(self.this_circle)

        self.uniformity = uniformity_on_circumference(self.points)

        if self.last_circle >= 0.:
            self.distance = abs(self.this_circle - self.last_circle)
            if self.distance >= .5:
                self.distance = 1. - self.distance
            self.average_distance = (self.average_distance * self.iteration + self.distance) / (self.iteration + 1)
        self.iteration += 1

    def _main_circle(self) -> None:
        x_mid = self.width // 2
        y_mid = self.height // 2
        r = min(x_mid, y_mid) * .8
        Canvas.circle(x_mid, y_mid, r, (255, 255, 255, 255))
        pyglet.graphics.draw(
            2, pyglet.gl.GL_LINES,
            ("v2f", (x_mid + r - 10., y_mid, x_mid + r + 10., y_mid))
        )

    def _on_draw(self) -> None:
        x_mid = self.width // 2
        y_mid = self.height // 2
        r = min(x_mid, y_mid) * .8

        self.fade()
        self._main_circle()

        if self.last_circle >= 0.:
            from_x, from_y = linear_to_circular(0., 0., self.last_circle, radius=r)
            to_x, to_y = linear_to_circular(0., 0., self.this_circle, radius=r)
            Canvas.circle(x_mid + to_x, y_mid + to_y, 10., (255, 255, 255, 255))
            pyglet.graphics.draw(
                2, pyglet.gl.GL_LINES,
                ("v2f", (from_x + x_mid, from_y + y_mid, to_x + x_mid, to_y + y_mid)),
                ("c4B", (255, 255, 255, 128,
                         255, 255, 255, 128))
            )
            label = pyglet.text.Label(
                f"{self.iteration:d}, {self.distance=:.4f}, {self.average_distance=:.4f}, {self.uniformity=:.4f}, product: {self.average_distance * self.uniformity:.4f}",
                x=2, y=2, font_size=16, color=(255, 255, 255, 255))
            label.draw()

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        self.mouse_released = True


def main():
    canvas = SpreadCanvas(width=1024, height=768, updates_per_second=60)
    canvas.run()


if __name__ == '__main__':
    main()
