from abc import ABC, abstractmethod
from typing import Any


class ViewProvider(ABC):
    @abstractmethod
    def render(
            self,
            template: str,
            **context: Any,
    ) -> str:
        pass
