from pathlib import Path

from src.dtos.ingest_request import IngestRequest
from src.rules.ingest_rule import IngestRule


class DirectoryExistsRule(IngestRule):
    def validate(self, dto: IngestRequest) -> None:
        path = Path(dto.path)

        if not path.exists():
            raise FileNotFoundError(f'O diretório `{dto.path}` não existe.')

        if not path.is_dir():
            raise NotADirectoryError(f'`{dto.path}` não é um diretório.')
