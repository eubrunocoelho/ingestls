from flask import Blueprint

from src.container.di_container import ingest_controller

ingest_bp: Blueprint = Blueprint('ingest_routes', __name__)


@ingest_bp.route('/ingest', methods=['GET'])
def index():
    return ingest_controller.index()


@ingest_bp.route('/ingest', methods=['POST'])
def create():
    return ingest_controller.create()
