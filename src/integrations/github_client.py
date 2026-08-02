from abc import ABC, abstractmethod

from src.dtos.github_tree_item_dto import GitHubTreeItemDTO


class GitHubClient(ABC):
    @abstractmethod
    def repository_exists(self, owner: str, repo: str) -> bool:
        pass

    @abstractmethod
    def get_default_branch(self, owner: str, repo: str) -> str:
        pass

    @abstractmethod
    def get_repository_tree(self, owner: str, repo: str, branch: str) -> list[GitHubTreeItemDTO]:
        pass

    @abstractmethod
    def get_blob_content(self, owner: str, repo: str, sha: str) -> bytes:
        pass
