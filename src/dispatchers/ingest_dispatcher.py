from src.dtos.ingest_request_dto import IngestRequestDTO
from src.dtos.ingest_response_dto import IngestResponseDTO
from src.strategies.ingest_strategy import IngestStrategy


class IngestDispatcher:
    def __init__(self, *strategies: IngestStrategy):
        self.strategies = strategies

    def dispatch(self, dto: IngestRequestDTO) -> IngestResponseDTO:
        for strategy in self.strategies:
            if strategy.supports(dto):
                return strategy.ingest(dto)

        raise RuntimeError('Nenhuma estratégia encontrada.')
