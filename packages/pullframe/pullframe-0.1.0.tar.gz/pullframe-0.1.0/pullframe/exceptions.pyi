# isort:skip_file
from typing import Any, List

from pullframe.types import Demand as Demand
from pullframe.types import Node as Node

class AllSyncFailed(Exception):
    nodes: List[Node]
    demand: Demand
    def __init__(self, nodes: Any, demand: Any) -> None: ...

class NoResourceAvailable(Exception):
    demand: Demand
    def __init__(self, demand: Any) -> None: ...
