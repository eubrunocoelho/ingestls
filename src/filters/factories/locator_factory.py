from src.enums.pattern_scope_enum import PatternScopeEnum
from src.filters.locators.locator import Locator


class LocatorFactory:
    def __init__(self):
        self._locators: dict[PatternScopeEnum, Locator] = {
            PatternScopeEnum.GLOBAL: GlobalLocator(),
            PatternScopeEnum.RECURSIVE: RecursiveLocator(),
            PatternScopeEnum.PATH: PathLocator(),
        }

    def make(self, scope: PatternScopeEnum) -> Locator:
        try:
            return self._locators[scope]
        except KeyError:
            raise ValueError(
                f'Locator não encontrado para \'{scope.value}\'.'
            )
