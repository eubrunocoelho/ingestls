from flask import Flask

import src.helpers.functions

from src.handlers.global_exception_handler import GlobalExceptionHandler
from src.routes.ingest_routes import ingest_bp
from src.routes.web_routes import web_bp

app: Flask = Flask(__name__)

GlobalExceptionHandler.init_app(app)

app.register_blueprint(web_bp)
app.register_blueprint(ingest_bp)

if __name__ == '__main__':
    app.run(debug=True)
