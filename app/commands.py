from flask import current_app
from app import db, bcrypt
from app.models import User

def register_commands(app):
    @app.cli.command("create-admin")
    def create_admin():
        """Vytvoří administrátorský účet."""
        with app.app_context():
            existing_admin = User.query.filter_by(email="admin@artemoderno.com").first()
            if existing_admin:
                print("Admin účet již existuje.")
                return

            hashed_password = bcrypt.generate_password_hash("arte2024").decode("utf-8")
            admin = User(username="admin", email="admin@artemoderno.com", password=hashed_password, role='admin')
            db.session.add(admin)
            db.session.commit()
            print("Admin účet byl úspěšně vytvořen!")
