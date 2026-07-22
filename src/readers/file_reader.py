from abc import ABC, abstractmethod

from src.dtos.ingest_request_dto import IngestRequestDTO


class FileReader(ABC):
    @abstractmethod
    def read(self, dto: IngestRequestDTO) -> str:
        pass
