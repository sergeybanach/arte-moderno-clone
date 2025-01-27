from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Registrace blueprintů
    from app.views.routes import views
    app.register_blueprint(views)

    return app