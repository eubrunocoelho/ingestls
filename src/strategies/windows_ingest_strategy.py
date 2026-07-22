from pathlib import Path

from src.dtos.ingest_request_dto import IngestRequestDTO
from src.strategies.ingest_strategy import IngestStrategy


class WindowsIngestStrategy(IngestStrategy):
    def supports(self, dto: IngestRequestDTO) -> bool:
        path = Path(dto.path)

        print('PATH:', dto.path)
        print('DRIVE:', path.drive)

        return Path(dto.path).drive != ''

    def ingest(self, dto: IngestRequestDTO) -> None:
        print(f'Ingerindo arquivos de `{dto.path}`')
