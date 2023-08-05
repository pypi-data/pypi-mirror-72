# isort:skip_file
from datetime import datetime
from enum import Enum
from pydantic import BaseModel  # type:ignore
from typing import List, Optional

class CacheFormat(str, Enum):
    PYTABLES: str = ...

class Node(BaseModel):
    host: str
    directory: str

class Demand(BaseModel):
    cache_format: CacheFormat
    name: str
    start: Optional[datetime] = ...
    end: Optional[datetime] = ...

class Request(BaseModel):
    source: Node
    directory: str
    demand: Demand

class Resource(BaseModel):
    nodes: List[Node]
    version: int
    last_idx: datetime
