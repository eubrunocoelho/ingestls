from src.enums.pattern_type_enum import PatternTypeEnum

STRATEGY_METHOD_BY_PATTERN_TYPE: dict[PatternTypeEnum, str] = {
    PatternTypeEnum.INCLUDE: 'include',
    PatternTypeEnum.EXCLUDE: 'exclude',
}
