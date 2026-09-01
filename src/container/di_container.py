from typing import Any, Callable

from src.container.binding import Binding
from src.container.lifetime import Lifetime


class DIContainer:
    def __init__(self):
        self._bindings: dict[type, Binding] = {}

    def singleton(self, abstract: type, factory: Callable[[], Any]) -> None:
        self._bindings[abstract] = Binding(
            factory=factory,
            lifetime=Lifetime.SINGLETON,
        )

    def bind(self, abstract: type, factory: Callable[[], Any]) -> None:
        self._bindings[abstract] = Binding(
            factory=factory,
            lifetime=Lifetime.TRANSIENT,
        )

    def resolve(self, abstract: type) -> Any:
        binding = self._bindings.get(abstract)

        if binding is None:
            raise RuntimeError(
                f'Abstração não vinculada para {abstract.__name__}',
            )

        if (
                binding.lifetime == Lifetime.SINGLETON
                and binding.instance is not None
        ):
            return binding.instance

        instance = binding.factory()

        if binding.lifetime == Lifetime.SINGLETON:
            binding.instance = instance

        return instance
