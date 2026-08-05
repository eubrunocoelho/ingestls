from src.dtos.github_tree_item_dto import GitHubTreeItemDTO
from src.integrations.github_client import GitHubClient
from src.integrations.github_http_client import GitHubHTTPClient
from src.services.github_blob_service import GitHubBlobService
from src.services.github_repository_service import GitHubRepositoryService

class GitHubAPIClient(GitHubClient):
    def __init__(self, http: GitHubHTTPClient):
        self.repository = GitHubRepositoryService(http)
        self.blob = GitHubBlobService(http)

    def repository_exists(self, owner: str, repo: str) -> bool:
        return self.repository.exists(owner, repo)

    def get_default_branch(self, owner: str, repo: str) -> str:
        return self.repository.default_branch(owner, repo)

    def get_repository_tree(self, owner: str, repo: str, branch: str) -> list[GitHubTreeItemDTO]:
        return self.repository.tree(owner, repo, branch)

    def get_blob_content(self, owner: str, repo: str, sha: str) -> bytes:
        return self.blob.content(owner, repo, sha)
