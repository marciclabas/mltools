from typing import Any
from pydantic import BaseModel

class Meta(BaseModel):
  class Files(BaseModel):
    inputs: str
    labels: str
  samples: int
  meta: Any | None = None
  files: Files