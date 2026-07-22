from flask import Blueprint

from services.ingest_service import IngestService
from src.controllers.ingest_controller import IngestController

ingest_service = IngestService()
ingest_controller = IngestController()
ingest_bp: Blueprint = Blueprint('ingest_routes', __name__)


@ingest_bp.route('/ingest', methods=['GET'])
def index():
    return ingest_controller.index()


@ingest_bp.route('/ingest', methods=['POST'])
def create():
    return ingest_controller.create()
