from abc import ABC, abstractmethod

from src.dtos.ingest_request import IngestRequest

class IngestRule(ABC):
    @abstractmethod
    def validate(self, dto: IngestRequest) -> None:
        pass
