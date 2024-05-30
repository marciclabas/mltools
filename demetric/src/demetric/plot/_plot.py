from typing import NamedTuple, Mapping
import pandas as pd
from matplotlib import axes as ax, figure as fig, pyplot as plt

class Plot(NamedTuple):
  fig: fig.Figure
  ax: ax.Axes

def metric(df: pd.DataFrame):
  fig, ax = plt.subplots()
  ax.plot(df['step'], df['value'])
  return Plot(fig, ax)

def metrics(metrics: Mapping[str, pd.DataFrame]):
  fig, ax = plt.subplots()
  for name, df in metrics.items():
    ax.plot(df['step'], df['value'], label=name)
  return Plot(fig, ax)