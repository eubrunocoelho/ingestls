from flask import Flask, jsonify

from src.handlers.global_exception_handler import GlobalExceptionHandler
from src.routes.ingest_routes import ingest_bp

app = Flask(__name__)

GlobalExceptionHandler.init_app(app)

app.register_blueprint(ingest_bp)

if __name__ == '__main__':
    app.run(debug=True)
