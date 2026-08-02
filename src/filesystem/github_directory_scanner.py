from src.dtos.github_tree_item_dto import GitHubTreeItemDTO
from src.filesystem.directory_node import DirectoryNode
from src.integrations.github_client import GitHubClient


class GitHubDirectoryScanner:
    def __init__(self, github_client: GitHubClient):
        self.github_client = github_client

    def read(self, owner: str, repo: str, branch: str | None = None) -> DirectoryNode:
        resolved_branch = branch or self.github_client.get_default_branch(owner, repo)
        items = self.github_client.get_repository_tree(owner, repo, resolved_branch)

        root = DirectoryNode(name=repo, is_directory=True, path='')
        nodes_by_path: dict[str, DirectoryNode] = {'': root}

        for item in sorted(items, key=lambda entry: entry.path.count('/')):
            self._insert(item, nodes_by_path)

        self._sort_recursively(root)

        return root

    @staticmethod
    def _insert(item: GitHubTreeItemDTO, nodes_by_path: dict[str, DirectoryNode]) -> None:
        parent_path, _, name = item.path.rpartition('/')
        parent = nodes_by_path.get(parent_path, nodes_by_path[''])

        node = DirectoryNode(
            name=name,
            is_directory=item.type == 'tree',
            path=item.path,
        )

        parent.children.append(node)
        nodes_by_path[item.path] = node

    def _sort_recursively(self, node: DirectoryNode) -> None:
        node.children.sort(key=lambda item: (not item.is_directory, item.name.lower()))

        for child in node.children:
            if child.is_directory:
                self._sort_recursively(child)
