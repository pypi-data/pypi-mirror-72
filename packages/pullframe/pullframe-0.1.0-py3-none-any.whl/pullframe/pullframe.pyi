# isort:skip_file
import pandas as pd  # type: ignore
import requests
from datetime import datetime
from pullframe.api import Coordinator as Coordinator, Persist as Persist
from typing import Optional
from pullframe.types import Node as Node

class _PullFrame:
    persist: Persist
    coordinator: Coordinator
    client: requests.Session
    sync_timeo: float
    node: Node = ...
    def __post_init__(self) -> None: ...
    def load(
        self,
        name: str,
        start: Optional[datetime] = ...,
        end: Optional[datetime] = ...,
    ) -> pd.DataFrame: ...
    def save(self, name: str, df: pd.DataFrame) -> None: ...
    def __init__(
        self,
        persist: Persist,
        coordinator: Coordinator,
        client: requests.Session,
        sync_timeo: float,
    ) -> None: ...
