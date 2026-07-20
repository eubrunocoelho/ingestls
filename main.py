from flask import Flask
from src.routes.ingest_routes import ingest_bp

app = Flask(__name__)

app.register_blueprint(ingest_bp)

if __name__ == '__main__':
    app.run(debug=True)
