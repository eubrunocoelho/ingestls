from flask import Blueprint, Response

from src.helpers.functions import get_container
from src.controllers.ingest_controller import IngestController

ingest_bp = Blueprint('ingest_routes', __name__)


@ingest_bp.route('/ingest', methods=['POST'])
def create() -> tuple[Response, int]:
    controller = get_container().resolve(IngestController)

    return controller.create()
