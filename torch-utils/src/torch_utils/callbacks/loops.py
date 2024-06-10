from typing import TypeVar, TypeAlias, Callable, Iterable, Sequence

X = TypeVar('X')

Callback: TypeAlias = Callable[[int], None]

def every(steps: int, cb: Callback, *, do_first: bool = False) -> Callback:
  """Run a callback `cb` every `steps` steps"""
  def _cb(step: int) -> None:
    if step % steps == 0 and (do_first or step > 0):
      cb(step)
  return _cb

def loop(
  step: Callable[[X], None], data: Iterable[X],
  *, callbacks: Sequence[Callback] = []
):
  """Simple loop with callbacks"""
  for i, x in enumerate(data):
    step(x)
    for cb in callbacks:
      cb(i)