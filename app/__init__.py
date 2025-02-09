from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Inicializace rozšíření (zatím bez propojení s aplikací)
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Propojení rozšíření s aplikací
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "views.login"
    login_manager.login_message_category = "info"

    # Import modelů Až po inicializaci db, aby se předešlo kruhovým importům
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import CLI příkazů
    from app.commands import register_commands
    register_commands(app)

    # Import blueprintů po inicializaci db
    from app.views.routes import views
    from app.views.admin_routes import admin
    from app.views.cart_routes import cart

    app.register_blueprint(views)
    app.register_blueprint(admin)
    app.register_blueprint(cart)

    return app
