from src.enums.pattern_scope_enum import PatternScopeEnum
from src.filters.locators.global_locator import GlobalLocator
from src.filters.locators.locator import Locator
from src.filters.locators.path_locator import PathLocator
from src.filters.locators.recursive_locator import RecursiveLocator


class LocatorFactory:
    def __init__(self):
        self._locators: dict[PatternScopeEnum, Locator] = {
            PatternScopeEnum.GLOBAL: GlobalLocator(),
            PatternScopeEnum.RECURSIVE: RecursiveLocator(),
            PatternScopeEnum.PATH: PathLocator(),
        }

    def make(self, scope: PatternScopeEnum) -> Locator:
        locator = self._locators.get(scope)

        if locator is None:
            raise ValueError(
                f'Locator não encontrado para \'{scope.value}\'.',
            )

        return locator
