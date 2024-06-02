from typing import Mapping, Iterable
import pandas as pd
from . import Metrics

def adj_concat(dfs: Iterable[pd.DataFrame], copy: bool = False) -> pd.Series:
  """Concatenate series with cumulative index"""
  cum_idx = 0
  adj_dfs = []

  for df in dfs:
    last_idx = df.index[-1]
    adj_df = df.copy() if copy else df
    adj_df.index = adj_df.index + cum_idx
    cum_idx += last_idx + 1
    adj_dfs.append(adj_df)

  return pd.concat(adj_dfs)

def compare(runs: Mapping[str, Metrics], metric: str):
  """Concat runs' dataframes by column, prepending the run's id to the column names"""
  dfs = { id: df for id, run in runs.items() if (df := run.read(metric)) is not None }
  return pd.concat(dfs, axis=1)

def concat(runs: Iterable[Metrics], metric: str):
  """Concat runs' dataframes by row, adjusting the index"""
  dfs = [df for run in runs if (df := run.read(metric)) is not None]
  return adj_concat(dfs)