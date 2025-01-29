from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Vytvoření instancí (ale ještě je nepropojujeme s aplikací)
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializace rozšíření s aplikací
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Nastavení login_view (kam se nepřihlášený uživatel přesměruje)
    login_manager.login_view = "views.login"
    # Volitelně: kategorie pro flash zprávu
    login_manager.login_message_category = "info"

    # Import modelů AŽ PO inicializaci db, abychom předešli kruhovým importům
    with app.app_context():
        from app.models import User  # User i Inquiry, ale stačí pro user_loader

        @login_manager.user_loader
        def load_user(user_id):
            # Funkce, kterou volá Flask-Login k načtení uživatele ze session
            return User.query.get(int(user_id))

    # Registrace blueprintů
    from app.views.routes import views
    app.register_blueprint(views)

    return app
