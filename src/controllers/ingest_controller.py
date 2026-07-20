from flask import jsonify


class IngestController:
    @staticmethod
    def index():
        return jsonify({
            'message': 'Olá, mundo!',
        })
