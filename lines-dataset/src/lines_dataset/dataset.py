from typing_extensions import Iterable, Mapping, TypeVar, LiteralString
from dataclasses import dataclass
import os
from haskellian import Iter, iter as I, dicts as D
from .meta import Meta

K = TypeVar('K', bound=LiteralString)

@dataclass
class Dataset(Iterable[Mapping[str, str]]):

  base_path: str
  files: Mapping[str, Meta.File]

  @classmethod
  def read(cls, base: str) -> 'Dataset':
    with open(os.path.join(base, 'meta.json')) as f:
      meta = Meta.model_validate_json(f.read())
    return Dataset(base, meta.lines_dataset)
  
  def file(self, key: str) -> Meta.File | None:
    """Metadata of a given file"""
    if key in self.files:
      file = self.files[key]
      return Meta.File(file=os.path.join(self.base_path, file.file), compression=file.compression)
    return None
  
  @I.lift
  def iterate(self, key: str) -> Iterable[str]:
    """Iterate lines of a single file."""
    file = self.file(key)
    if file:
      if file.compression == 'zstd':
        from .compression import iterate
        yield from iterate(file.file)
      else:
        with open(file.file) as f:
          yield from f

  def samples(self, *keys: K) -> Iter[Mapping[K, str]]:
    """Iterate all samples of `keys`. If no `keys` are provided, iterates all files."""
    keys = keys or list(self.files.keys()) # type: ignore
    return D.zip({
      k: self.iterate(k)
      for k in keys
    })

  def __iter__(self):
    return iter(self.samples())

  def len(self, *keys: str) -> int | None:
    """Returns the minimum length of `keys` (or all files, if not provided). Returns `None` if some length is unspecified, or if some key is not found"""
    keys = keys or list(self.files.keys()) # type: ignore
    lens = [self._len(k) for k in keys]
    if None in lens:
      return None
    return min(lens) # type: ignore

  def _len(self, key: str) -> int | None:
    file = self.file(key)
    return file and file.num_lines