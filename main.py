from flask import Flask, jsonify

from src.handlers.validation_handler import register_validation_handler
from src.routes.ingest_routes import ingest_bp

app = Flask(__name__)

register_validation_handler(app)
app.register_blueprint(ingest_bp)

if __name__ == '__main__':
    app.run(debug=True)
