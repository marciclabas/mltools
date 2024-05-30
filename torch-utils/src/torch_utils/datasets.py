from typing import Generic, TypeVar, Callable, Iterable
from torch.utils.data import Dataset, IterableDataset

T = TypeVar('T')

class LazyDataset(Dataset[T], Generic[T]):
  def __init__(
    self, sample: Callable[[int], T], num_samples: int
  ):
    self.samples: dict[int, T] = {}
    self.sample = sample
    self.num_samples = num_samples

  def __len__(self):
    return self.num_samples

  def __getitem__(self, idx: int) -> T:
    if idx in self.samples:
      return self.samples[idx]
    else:
      x = self.sample(idx)
      self.samples[idx] = x
      return x
    
class IterDataset(IterableDataset[T], Generic[T]):
  def __init__(self, samples: Callable[[], Iterable[T]], num_samples: int):
    self.samples = samples
    self.num_samples = num_samples

  def __len__(self):
    return self.num_samples

  def __iter__(self):
    return iter(self.samples())