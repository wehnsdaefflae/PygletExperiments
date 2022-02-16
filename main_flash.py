from tools.drawing import Canvas


class FlashCanvas(Canvas):
  def __init__(self, *args, updates_per_second: int = 10, **kwargs):
    super().__init__(*args, updates_per_second=updates_per_second, **kwargs)
    self.phases = {
      "black":        1, 
      "ignition":     1, 
      "black":        1, 
      "blind":        1, 
      "broad_stroke": 1, 
      "strike":       3, 
      "fizzle":       1, 
      "dissolve":     7, 
      "fizzle":       3
      }
      
    
  def _update(self, dt: float) -> None:
    return super()._update(dt)
  
  def _on_draw(self) -> None:
    return super()._on_draw()


def main():
  canvas = FlashCanvas(width=600, height=800)
  canvas.run()


if __name__ == "__main__":
  main()
