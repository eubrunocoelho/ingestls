from flask import Blueprint
from src.controllers.ingest_controller import IngestController

ingest_bp = Blueprint('ingest_routes', __name__)


@ingest_bp.route('/ingest', methods=['GET'])
def index():
    return IngestController.index()
