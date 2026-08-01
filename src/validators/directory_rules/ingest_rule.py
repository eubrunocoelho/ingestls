from abc import ABC, abstractmethod

from src.dtos.ingest_request_dto import IngestRequestDTO


class IngestRule(ABC):
    @abstractmethod
    def supports(self, dto: IngestRequestDTO) -> bool:
        pass

    @abstractmethod
    def validate(self, dto: IngestRequestDTO) -> None:
        pass
