from flask import Blueprint

from src.container.di_container import web_controller

web_bp = Blueprint('web_routes', __name__)


@web_bp.route('/', methods=['GET'])
def index():
    return web_controller.index()
