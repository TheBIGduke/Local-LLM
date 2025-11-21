from __future__ import annotations
from typing import Dict, Any, Optional, Callable
import logging

class GetInfo:
    def __init__(self) -> None:
        self.log = logging.getLogger("Publish") 
        pass

    # You can add new tools here in the future.