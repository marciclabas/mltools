from typing import Iterable, Sequence, Mapping, TypeVar, LiteralString
from dataclasses import dataclass
import os
from glob import glob
import fs
from .meta import Meta

K = TypeVar('K', bound=LiteralString)

def zip_files(files: Mapping[str, Sequence[str]]) -> Iterable[Mapping[str, str]]:
  iters = {
    key: iter(fs.concat_lines(file))
    for key, file in files.items()
  }
  while True:
    try:
      yield {
        key: next(it)
        for key, it in iters.items()
      }
    except StopIteration:
      break

@dataclass
class Dataset(Iterable[Mapping[str, str]]):

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
  
  def keys(self):
    return list(self.meta.files.keys())
  
  def files(self, key: str) -> Sequence[str]:
    if key in self.meta.files:
      return glob(os.path.join(self.base_path, self.meta.files[key]))
    return []
  
  def iterate(self, key: str) -> Iterable[str]:
    yield from fs.concat_lines(self.files(key))

  def samples(self, *keys: K) -> Iterable[Mapping[K, str]]:
    keys = keys or list(self.meta.files.keys())
    files = {
      key: self.files(key)
      for key in keys
    }
    yield from zip_files(files)

  def __iter__(self) -> Iterable[Mapping[str, str]]:
    return self.samples()

  def __len__(self) -> int:
    return self.meta.samples