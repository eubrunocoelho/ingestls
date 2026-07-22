from abc import ABC, abstractmethod

from src.dtos.ingest_request_dto import IngestRequestDTO


class IngestStrategy(ABC):
    @abstractmethod
    def supports(self, dto: IngestRequestDTO) -> bool:
        pass

    @abstractmethod
    def ingest(self, dto: IngestRequestDTO) -> None:
        pass
