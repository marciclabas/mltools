from typing import Sequence
import pandas as pd
from . import Run

def readall(runs: Sequence[Run], metric: str) -> list[pd.Series]:
  """Read all runs' dataframes for a metric"""
  return [s.rename(run.id) for run in runs if (s := run.read(metric)) is not None]

def adj_concat(series: Sequence[pd.Series], copy: bool = False) -> pd.Series:
  """Concatenate series with cumulative index"""
  cum_idx = 0
  adj_series = []

  for s in series:
    last_idx = s.index[-1]
    adj_s = s.copy() if copy else s
    adj_s.index = adj_s.index + cum_idx
    cum_idx += last_idx + 1 # type: ignore
    adj_series.append(adj_s)

  return pd.concat(adj_series) # type: ignore

def compare(runs: Sequence[Run], metric: str):
  """Concat runs' dataframes by column, prepending the run's id to the column names"""
  series = readall(runs, metric)
  return pd.concat(series, axis=1)

def concat(runs: Sequence[Run], metric: str):
  """Concat runs' dataframes by row, adjusting the index"""
  dfs = readall(runs, metric)
  return adj_concat(dfs)