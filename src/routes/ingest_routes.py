from flask import Blueprint
from flask.typing import ResponseReturnValue
from src.controllers.ingest_controller import IngestController

ingest_bp: Blueprint = Blueprint('ingest_routes', __name__)


@ingest_bp.route('/ingest', methods=['GET'])
def index() -> ResponseReturnValue:
    return IngestController.index()


@ingest_bp.route('/ingest', methods=['POST'])
def create() -> ResponseReturnValue:
    return IngestController.create()
