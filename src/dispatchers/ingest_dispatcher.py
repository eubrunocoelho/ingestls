from src.dtos.ingest_request_dto import IngestRequestDTO
from src.strategies.ingest_strategy import IngestStrategy


class IngestDispatcher:
    def __init__(self, *strategies: IngestStrategy):
        self.strategies = strategies

    def dispatch(self, dto: IngestRequestDTO) -> None:
        for strategy in self.strategies:
            if strategy.supports(dto):
                strategy.ingest(dto)

                return

        raise RuntimeError('Nenhuma estratégia encontrada.')
