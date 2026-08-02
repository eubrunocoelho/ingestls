from src.filesystem.content_inspector import ContentInspector
from src.filesystem.directory_node import DirectoryNode
from src.integrations.github_client import GitHubClient


class GitHubFileReader:
    _FILE_INFO = (
        '================================================\n'
        'FILE: {filename}\n'
        'DIRECTORY: {directory}\n'
        '================================================'
    )

    _BINARY_FILE_FLAG = '[Binary File]'
    _EMPTY_FILE_FLAG = '[Empty File]'

    def __init__(
            self,
            github_client: GitHubClient,
            content_inspector: ContentInspector
    ):
        self.github_client = github_client
        self.content_inspector = content_inspector

    def read(
            self,
            tree: DirectoryNode,
            owner: str,
            repo: str
    ) -> str:
        contents: list[str] = []

        self._collect(tree, owner, repo, contents)

        return '\n'.join(contents)

    def _collect(
            self,
            node: DirectoryNode,
            owner: str,
            repo: str,
            contents: list[str]
    ) -> None:
        for child in node.children:
            if child.is_directory:
                self._collect(child, owner, repo, contents)

                continue

            directory, _, _ = child.path.rpartition('/')
            directory_display = './' if not directory else directory

            contents.append(self._FILE_INFO.format(
                filename=child.name,
                directory=directory_display,
            ))

            contents.append(self._read_contents(child, owner, repo))

    def _read_contents(
            self,
            node: DirectoryNode,
            owner: str,
            repo: str
    ) -> str:
        raw_content = self.github_client.get_blob_content(owner, repo, node.sha)

        if self.content_inspector.is_empty(raw_content):
            return self._EMPTY_FILE_FLAG

        if self.content_inspector.is_binary(raw_content):
            return self._BINARY_FILE_FLAG

        return raw_content.decode('utf-8')
