from dataclasses import dataclass

from src.dtos.pattern_dto import PatternDTO
from src.filters.locators.locator import Locator
from src.filters.matchers.matcher import Matcher


@dataclass(frozen=True, slots=True)
class CompiledPatternDTO:
    locator: Locator
    matcher: Matcher
    pattern: PatternDTO
