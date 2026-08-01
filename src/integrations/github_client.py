from abc import ABC, abstractmethod


class GitHubClient(ABC):
    @abstractmethod
    def repository_exists(self, owner: str, repo: str) -> bool:
        pass
