from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_mail import Mail

# 1) Vytvoříme instanci SQLAlchemy a Migrate
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()  # <-- vytvoříme objekt Mail

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 2) Napojíme db a migrate na aplikaci
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)  # <-- zaregistrujeme Flask-Mail s aplikací

    # Načtení modelů (stačí až po inicializaci db)
    from app import models

    # Registrace blueprintů
    from app.views.routes import views
    app.register_blueprint(views)

    return app
