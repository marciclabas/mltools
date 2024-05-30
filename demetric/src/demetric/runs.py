from typing import Sequence
from dataclasses import dataclass
import os
from .run import Run

@dataclass
class Runs:
  base_path: str

  def __post_init__(self):
    os.makedirs(self.base_path, exist_ok=True)

  def ids(self) -> Sequence[str]:
    return os.listdir(self.base_path)

  def runs(self) -> Sequence[Run]:
    return [Run(id, self.base_path) for id in self.ids()]
  
  def run(self, id: str) -> Run:
    return Run(id, self.base_path)