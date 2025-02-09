import os
from flask_login import UserMixin
from datetime import datetime
from app import db  # ✅ Opraveno - už nevoláme db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # Přidali jsme role
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"


class Inquiry(db.Model):
    """Tabulka dotazů od zákazníků."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(150))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Inquiry from {self.name}, {self.email}>"

class Product(db.Model):
    """Tabulka produktů (obrazy, sochy) v e-shopu."""
    id = db.Column(db.Integer, primary_key=True)
    position_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image_filename = db.Column(db.String(300), nullable=True)  # Název souboru obrázku
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_image_url(self):
        """Vrací URL obrázku nebo placeholder, pokud obrázek není nahrán."""
        if self.image_filename:
            return f"/static/uploads/{self.image_filename}"
        return "/static/images/placeholder.png"

    def __repr__(self):
        return f"<Product {self.name}, Position {self.position_id}>"
    
from app import db

class CartItem(db.Model):
    """Tabulka pro položky v košíku"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))

    def __repr__(self):
        return f"<CartItem User {self.user_id}, Product {self.product_id}, Qty {self.quantity}>"

