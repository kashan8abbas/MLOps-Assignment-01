from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)

    from .app import bp as app_bp  # noqa: WPS433

    app.register_blueprint(app_bp)
    return app
