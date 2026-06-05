from flask import Flask
from flask_cors import CORS
from app.config import Config


def create_app() -> Flask:
    """Application factory."""
    flask_app = Flask(__name__)

    # CORS
    CORS(flask_app, origins=Config.ALLOWED_ORIGINS, supports_credentials=True)

    # Trigger Firebase + SQLAlchemy initialisation (side-effect import)
    from app import extensions  # noqa: F401

    # Register all blueprints
    from app.routes import register_blueprints
    register_blueprints(flask_app)

    return flask_app
