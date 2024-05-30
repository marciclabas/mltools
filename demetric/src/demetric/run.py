from typing import Sequence, Container, Mapping, NamedTuple, Any, overload
import os
from shutil import rmtree
import json
from . import plot

class Entry(NamedTuple):
  step: int
  value: float

class Run:

  id: str
  base_path: str
  overwrite: bool = False

  def __repr__(self):
    with open(self.meta_path) as f:
      meta = json.load(f)
    return f'Run({self.id}, {meta})'


  def __init__(
    self, id: str, base_path: str, *,
    meta: Any = None, overwrite: bool = False
  ):
    
    self.id = id
    self.base_path = base_path
    self.path = os.path.join(self.base_path, self.id)

    if overwrite:
      rmtree(self.path, ignore_errors=True)

    os.makedirs(self.path, exist_ok=True)
    if meta:
      with open(self.meta_path, 'w') as f:
        json.dump(meta, f, indent=2)

  @property
  def meta_path(self):
    return os.path.join(self.path, 'meta.json')

  @property
  def metrics_path(self):
    return os.path.join(self.path, 'metrics')

  def metric_path(self, metric: str):
    return os.path.join(self.metrics_path, f'{metric}.csv')

  def log(self, metric: str, *, value, step: int):

    path = self.metric_path(metric)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if not os.path.exists(path):
      with open(path, 'w') as f:
        f.write('step,value\n')
    
    with open(path, 'a') as f:
      f.write(f'{step},{value}\n')


  def read(self, metric: str):
    import pandas as pd
    return pd.read_csv(self.metric_path(metric))
  
  @overload
  def plot(self, metric: str) -> 'plot.Plot':
    """Plot `metric`"""
  @overload
  def plot(self, metrics: Sequence[str]) -> 'plot.Plot':
    """Plot all `metrics` into a same plot"""
  @overload
  def plot(self, *, without_metrics: Container[str]) -> 'plot.Plot':
    """Plot all metrics except `without_metrics` into a same plot"""
  @overload
  def plot(self) -> 'plot.Plot':
    """Plot all metrics into a same plot"""

  def plot(self, metric=None, *, without_metrics=None):
    if metric is None:
      if without_metrics is not None:
        metrics = { m: self.read(m) for m in self.metrics() if m not in without_metrics }
        return self._plot_metrics(metrics)
      else:
        return self._plot_metrics(self.read_all())
    elif isinstance(metric, str):
      return self._plot_metric(metric)
    else:
      return self._plot_metrics({ m: self.read(m) for m in metric })

  def _plot_metric(self, metric: str):
    df = self.read(metric)
    p = plot.metric(df)
    p.ax.set_title(f'{self.id}: {metric} over steps')
    p.ax.set_xlabel('step')
    p.ax.set_ylabel(metric)
    return p

  def _plot_metrics(self, metrics: Mapping[str, Sequence[str]]):
    p = plot.metrics(metrics)
    p.ax.legend()
    p.ax.set_title(f'{self.id}: Metrics over steps')
    p.ax.set_xlabel('step')
    p.ax.set_ylabel('Metrics')
    return p

  def metrics(self) -> Sequence[str]:
    """List all metrics"""
    return [os.path.splitext(f)[0] for f in os.listdir(self.metrics_path)]
  
  def read_all(self):
    """Read all metrics as `pd.DataFrame` with columns `step` and `value`"""
    return { metric: self.read(metric) for metric in self.metrics() }