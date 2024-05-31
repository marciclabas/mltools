from typing import Any, Mapping, Literal
from pydantic import BaseModel

class Meta(BaseModel):
  
  class File(BaseModel):
    file: str
    compression: Literal['zstd'] | None = None

  samples: int
  meta: Any | None = None
  files: Mapping[str, File]