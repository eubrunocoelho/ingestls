from flask import jsonify
from pydantic import ValidationError


def register_validation_handler(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(e: ValidationError):
        return jsonify({
            "errors": e.errors()
        }), 400
