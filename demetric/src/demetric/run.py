from dataclasses import dataclass
import os
from glob import glob

@dataclass
class Run:

  path: str

  @property
  def id(self):
    return os.path.basename(os.path.abspath(self.path))
  
  def __repr__(self) -> str:
    return f'Run(id="{self.id}", path="{self.path}")'

  @classmethod
  def new(cls, path: str, overwrite: bool = False):
    exists = os.path.exists(path)
    if exists and not overwrite:
      raise FileExistsError(f'Run already exists at {path}. Use overwrite=True to overwrite it, or Run.append to append to it.')
    elif exists:
      csvs = glob(os.path.join(path, '*.csv'))
      for csv in csvs:
        os.remove(csv)
        
    os.makedirs(path, exist_ok=True)
    return Run(path)
  
  @classmethod
  def append(cls, path: str):
    if not os.path.exists(path):
      raise FileNotFoundError(f'Run does not exist at {path}')
    return Run(path)

  def metric_path(self, metric: str):
    return os.path.join(self.path, f'{metric}.csv')

  def log(self, metric: str, *, value, step: int):
    """Log a metric `value` at a `step`"""

    path = self.metric_path(metric)

    if not os.path.exists(path):
      with open(path, 'w') as f:
        f.write('step,value\n')
    
    with open(path, 'a') as f:
      f.write(f'{step},{value}\n')

  def read(self, metric: str):
    """Read `pd.DataFrame` for `metric`"""
    import pandas as pd
    try:
      return pd.read_csv(self.metric_path(metric), index_col='step')['value']
    except FileNotFoundError:
      ...

  def metrics(self) -> list[str]:
    """List all metrics"""
    return [
      os.path.splitext(os.path.split(f)[-1])[0]
      for f in glob(os.path.join(self.path, '*.csv'))
    ]

def is_run(path: str):
  return os.path.isdir(path) and glob(os.path.join(path, '*.csv')) != []

def runs(glob_: str) -> list[Run]:
  """Read all runs in a directory"""
  return [Run(p) for p in glob(glob_) if is_run(p)]