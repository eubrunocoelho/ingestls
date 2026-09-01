from dataclasses import asdict, is_dataclass
from http import HTTPStatus
from typing import Any

from flask import Response, jsonify


class ResponseFactory:
    @staticmethod
    def json(
            content: Any,
            status: HTTPStatus = HTTPStatus.OK,
    ) -> tuple[Response, int]:
        if is_dataclass(content):
            content = asdict(content)

        return jsonify(content), status.value
