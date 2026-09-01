from typing import Any

from flask import Blueprint, send_from_directory

from src.config.paths import ASSETS_PATH
from src.controllers.web_controller import WebController
from src.helpers.functions import get_container

web_bp = Blueprint('web_routes', __name__)


@web_bp.route('/', methods=['GET'])
def index():
    controller = get_container().resolve(WebController)

    return controller.index()


@web_bp.route('/assets/<path:filename>', methods=['GET'])
def assets(filename: str) -> Any:
    return send_from_directory(
        ASSETS_PATH,
        filename,
    )
