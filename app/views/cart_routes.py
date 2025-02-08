from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Product, CartItem
from app import db

cart = Blueprint("cart", __name__, url_prefix="/cart")

@cart.route("/add", methods=["POST"])
@login_required
def add_to_cart():
    data = request.get_json()
    product_id = data.get("product_id")

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Produkt nenalezen"}), 404

    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)

    db.session.commit()
    return jsonify({"message": "Produkt přidán do košíku"}), 200

@cart.route("/remove", methods=["POST"])
@login_required
def remove_from_cart():
    data = request.get_json()
    product_id = data.get("product_id")

    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if not cart_item:
        return jsonify({"error": "Produkt není v košíku"}), 404

    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"message": "Produkt odebrán z košíku"}), 200

@cart.route("/view", methods=["GET"])
@login_required
def view_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()

    cart_data = [
        {
            "id": item.id,
            "product_id": item.product.id,
            "name": item.product.name,
            "price": item.product.price,
            "quantity": item.quantity,
            "total_price": item.product.price * item.quantity
        }
        for item in cart_items
    ]

    return jsonify(cart_data), 200
