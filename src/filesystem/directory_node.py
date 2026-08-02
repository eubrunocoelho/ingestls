from dataclasses import dataclass, field


@dataclass(slots=True)
class DirectoryNode:
    name: str
    is_directory: bool
    path: str = ''
    sha: str = ''
    children: list["DirectoryNode"] = field(default_factory=list)
