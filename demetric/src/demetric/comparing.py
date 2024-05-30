from typing import Sequence
from .run import Run
from . import plot

def compare(runs: Sequence[Run], metric: str):
  p = plot.metrics({ r.id: r.read(metric) for r in runs })
  p.ax.set_title(f'{metric} comparison')
  p.ax.legend()
  p.ax.set_xlabel('step')
  p.ax.set_ylabel(metric)
  return p