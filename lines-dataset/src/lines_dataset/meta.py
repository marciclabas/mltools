from typing import Any, Mapping
from pydantic import BaseModel

class Meta(BaseModel):
  samples: int
  meta: Any | None = None
  files: Mapping[str, str]