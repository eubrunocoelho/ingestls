from flask import Blueprint, send_from_directory

from src.config.paths import ASSETS_PATH
from src.container.di_container import web_controller
web_bp = Blueprint('web_routes', __name__)


@web_bp.route('/', methods=['GET'])
def index():
    return web_controller.index()


@web_bp.route('/assets/<path:filename>', methods=['GET'])
def assets(filename: str):
    return send_from_directory(
        ASSETS_PATH,
        filename,
    )
