from src.dtos.ingest_request_dto import IngestRequestDTO
from src.dtos.ingest_response_dto import IngestResponseDTO
from src.strategies.ingest_strategy import IngestStrategy


class GitHubIngestStrategy(IngestStrategy):
    def supports(self, dto: IngestRequestDTO) -> bool:
        return dto.path.startswith('https://github.com/')

    def ingest(self, dto: IngestRequestDTO) -> IngestResponseDTO:
        raise NotImplementedError('GitHubIngestStrategy.ingest ainda não foi implementada.')
