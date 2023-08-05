# isort:skip_file
from datetime import datetime
from typing import Optional, Set, Any

from kazoo.client import KazooClient  # type: ignore

from pullframe.api import Coordinator as Coordinator
from pullframe.types import Node as Node
from pullframe.types import Resource as Resource

class _ZookeeperCoordinator(Coordinator):
    zk: KazooClient = ...
    def __init__(self, zk: KazooClient) -> None: ...
    def available(
        self, name: str, last_idx: Optional[datetime], version: int
    ) -> Optional[Resource]: ...
    def notify(
        self, name: str, node: Node, version: int, last_idx: datetime
    ) -> None: ...
    def version(self, name: str) -> Optional[int]: ...

def zookeeper_coordinator(
    hosts: Set[str] = ..., timeout: float = ...
) -> Any: ...
