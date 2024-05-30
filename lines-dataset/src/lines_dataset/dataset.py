from typing import Iterable, Sequence
from dataclasses import dataclass
import os
from glob import glob
import fs
from .meta import Meta

def iterate_samples(
  input_files: Sequence[str], label_files: Sequence[str],
) -> Iterable[tuple[str, str]]:
  inputs = fs.concat_lines(input_files)
  labels = fs.concat_lines(label_files)
  yield from zip(inputs, labels)

@dataclass
class Dataset:

  base_path: str
  meta: Meta

  @classmethod
  def read(cls, base: str) -> 'Dataset':
    with open(os.path.join(base, 'meta.json')) as f:
      meta = Meta.model_validate_json(f.read())
    return Dataset(base, meta)
  
  @classmethod
  def create(cls, base: str, meta: Meta, *, overwrite: bool = False) -> 'Dataset':
    os.makedirs(base, exist_ok=True)
    mode = 'x' if not overwrite else 'w'
    with open(os.path.join(base, 'meta.json'), mode) as f:
      f.write(meta.model_dump_json())
    return Dataset(base, meta)
  
  def input_files(self) -> Sequence[str]:
    return glob(os.path.join(self.base_path, self.meta.files.inputs))
  
  def label_files(self) -> Sequence[str]:
    return glob(os.path.join(self.base_path, self.meta.files.labels))

  def samples(self) -> Iterable[tuple[str, str]]:
    yield from iterate_samples(self.input_files(), self.label_files())