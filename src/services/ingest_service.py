from src.responses.ingest_response import IngestResponse
from src.dtos.ingest_request import IngestRequest


class IngestService:
    def ingest(self, dto: IngestRequest) -> IngestResponse:
        return IngestResponse(
            message='Olá, mundo!',
        )
