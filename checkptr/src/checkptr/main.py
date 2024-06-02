from typing import Callable, TypeVar, Generic
from dataclasses import dataclass
import os

Model = TypeVar('Model')

@dataclass
class Checkpointer(Generic[Model]):

  base_path: str
  save_fn: Callable[[Model, str], None]
  load_fn: Callable[[str], Model]

  @classmethod
  def pytorch(cls, base_path: str):
    import torch
    return cls(base_path, torch.save, torch.load)

  def path(self, name: str) -> str:
    return os.path.join(self.base_path, name)

  def checkpoint(self, model: Model, name: str):
    os.makedirs(self.base_path, exist_ok=True)
    self.save_fn(model, self.path(name))

  def load(self, name: str) -> Model:
    return self.load_fn(self.path(name))
  
  def checkpoints(self):
    return os.listdir(self.base_path)