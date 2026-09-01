from dataclasses import dataclass
from typing import Any, Callable

from src.container.lifetime import Lifetime


@dataclass
class Binding:
    factory: Callable[[], Any]
    lifetime: Lifetime
    instance: Any = None
