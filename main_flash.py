# coding=utf-8
from typing import Sequence
from tools.drawing import Canvas
import pyglet


class FlashCanvas(Canvas):
    def __init__(self, *args, updates_per_second: int = 10, **kwargs):
        super().__init__(*args, updates_per_second=updates_per_second, **kwargs)
        self.phases = (
            (self._black, 1),
            (self._ignition, 1),
            # (self._black, 1),
            # (self._blind, 1),
            # (self._broad_stroke, 3),
            # (self._strike, 1),
            # (self._fizzle, 7),
            # (self._dissolve, 11),
            # (self._black, 1),
        )

        self.no_phases = len(self.phases)

        self.current_phase_index = 0
        self.phase_frame_index = 0

        self.clear_next = False

    def _black(self, frame: int):
        ...

    @staticmethod
    def _path(*coordinates: tuple[int, int],
              x_scale: int = 1, y_scale: int = 1,
              width: int = 1,
              color: tuple[int, int, int] = (255, 255, 255), opacity: int = 255,
              batch: pyglet.graphics.Batch = None,
              group: pyglet.graphics.Group = None) -> Sequence[pyglet.shapes.Line]:

        no_coords = len(coordinates)
        lines = []
        for i in range(no_coords - 1):
            x0, y0 = coordinates[i]
            x1, y1 = coordinates[i + 1]

            each_line = pyglet.shapes.Line(
                x0 * x_scale, y0 * y_scale,
                x1 * x_scale, y1 * y_scale,
                width=width,
                color=color,
                batch=batch,
                group=group,
            )
            each_line.opacity = opacity
            lines.append(each_line)

        return lines

    def _ignition(self, frame: int):
        batch = pyglet.graphics.Batch()

        width = 2

        a_to_b = .5, .8
        coordinates = (.3, .85), (.5, 1.), (.1, .9), (.3, .85), a_to_b
        path_a = FlashCanvas._path(
            *coordinates,
            x_scale=self.width, y_scale=self.height,
            width=width,
            color=(255, 255, 255), opacity=255,
            batch=batch,
        )

        b_to_c = .45, .65
        coordinates = (.5, .7), a_to_b, (.7, .9), (.5, .7), b_to_c
        path_b = FlashCanvas._path(
            *coordinates,
            x_scale=self.width, y_scale=self.height,
            width=width,
            color=(255, 255, 255), opacity=255,
            batch=batch,
        )

        coordinates = (.4, .7), b_to_c, (.6, .7)
        path_c = FlashCanvas._path(
            *coordinates,
            x_scale=self.width, y_scale=self.height,
            width=width,
            color=(255, 255, 255), opacity=255,
            batch=batch,
        )

        batch.draw()

    def _blind(self, frame: int):
        ...

    def _broad_stroke(self, frame: int):
        ...

    def _strike(self, frame: int):
        ...

    def _fizzle(self, frame: int):
        ...

    def _dissolve(self, frame: int):
        ...

    def _update(self, dt: float) -> None:
        draw_phase, phase_end_frame = self.phases[self.current_phase_index]
        # print(f"{draw_phase.__name__:s} {self.phase_frame_index + 1:d} / {phase_end_frame:d}")

        self.phase_frame_index += 1
        if self.phase_frame_index >= phase_end_frame:
            self.current_phase_index = (self.current_phase_index + 1) % self.no_phases
            self.phase_frame_index = 0
            self.clear_next = True

    def _on_draw(self) -> None:
        draw_phase, phase_end_frame = self.phases[self.current_phase_index]
        if self.clear_next:
            self.clear_next = False
            self.clear()

        rectangle = pyglet.shapes.Rectangle(0, 0, self.width, 30, color=(10, 10, 10))
        rectangle.draw()
        label = pyglet.text.Label(
            text=f"{self.current_phase_index + 1:d} / {self.no_phases:d}: {draw_phase.__name__:s} {self.phase_frame_index + 1:d} / {phase_end_frame:d}",
            x=0,
            y=0,
            font_size=16,
            anchor_x="left",
            anchor_y="bottom",
            color=(255, 255, 255, 255)
        )
        label.draw()

        draw_phase(self.phase_frame_index)


def main():
    canvas = FlashCanvas(width=600, height=800, updates_per_second=2)
    canvas.run()


if __name__ == "__main__":
    main()
