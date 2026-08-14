from enum import Enum


class GitHubURLTypeEnum(str, Enum):
    REPOSITORY = 'repository'
    BRANCH = 'branch'
    TAG = 'tag'
    COMMIT = 'commit'
