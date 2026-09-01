from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader


class JinjaViewProvider:
    def __init__(self, views_path: Path):
        self.environment = Environment(
            loader=FileSystemLoader(views_path),
        )

    def render(
            self,
            template: str,
            **context: Any,
    ) -> str:
        return self.environment.get_template(template).render(
            **context,
        )
