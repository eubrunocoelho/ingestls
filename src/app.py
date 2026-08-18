from flask import Flask

from src.container.di_container import DIContainer
from src.handlers.global_exception_handler import GlobalExceptionHandler
from src.providers.app_service_provider import AppServiceProvider
from src.routes.ingest_routes import ingest_bp
from src.routes.web_routes import web_bp


def create_app() -> Flask:
    app = Flask(__name__)

    GlobalExceptionHandler.init_app(app)

    container = DIContainer()

    AppServiceProvider().register(container)

    app.extensions['container'] = container

    app.register_blueprint(web_bp)
    app.register_blueprint(ingest_bp)

    return app
