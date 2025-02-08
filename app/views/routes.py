from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models import Inquiry
from app import db, mail  # importujeme db a mail z __init__.py
from flask_mail import Message
from app import db, bcrypt
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from app.models import Product
from app.models import Inquiry, User, Product, CartItem


views = Blueprint("views", __name__)
cart = Blueprint("cart", __name__, url_prefix="/cart")

@views.route("/", methods=["GET"])
def home():
    return render_template("home.html")  # jen příklad

@views.route("/galerie")
def galerie():
    products = Product.query.all()  # ✅ Načítáme všechny produkty
    print("DEBUG: Produkty v galerii:")
    for product in products:
        print(f"ID: {product.id}, Název: {product.name}, Popis: {product.description}, Cena: {product.price}")
    
    return render_template("galerie.html", products=products)





@views.route("/kontakt", methods=["GET", "POST"])
def kontakt():
    if request.method == "POST":
        # 1. Získáme data z formuláře
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        # 2. Uložíme do DB
        new_inquiry = Inquiry(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        db.session.add(new_inquiry)
        db.session.commit()

        # 3. Odeslat e-maily

        # a) E-mail majiteli
        #    Odesílatel i příjemce bude stejný e-mail (váš), např. "artemodernoblaha@gmail.com"
        owner_msg = Message(
            subject=f"Nový dotaz od {name}",
            sender="artemodernoblaha@gmail.com",           # MUSÍ odpovídat MAIL_USERNAME v configu
            recipients=["artemodernoblaha@gmail.com"],     # stejné, aby došlo na váš mail
            body=(
                f"Nový dotaz od {name} (odeslal z e-mailu: {email}).\n\n"
                f"Předmět: {subject}\n\n"
                f"Znění zprávy:\n{message}\n\n"
                "Toto je automatická notifikace."
            )
        )
        mail.send(owner_msg)

        # b) E-mail klientovi (potvrzení)
        #    Odesílatel bude váš stejný e-mail, příjemcem je e-mail z formuláře
        client_msg = Message(
            subject="Děkujeme za váš dotaz",
            sender="artemodernoblaha@gmail.com",
            recipients=[email],
            body=(
                f"Dobrý den, {name},\n\n"
                f"Děkujeme za váš dotaz (předmět: {subject}).\n"
                "Brzy se vám ozveme a váš dotaz zodpovíme.\n\n"
                "S pozdravem,\n"
                "ArteModerní Tým"
            )
        )
        mail.send(client_msg)

        flash("Váš dotaz byl úspěšně odeslán!", "success")
        return redirect(url_for("views.kontakt"))

    # GET request => zobrazíme formulář
    return render_template("kontakt.html")

@views.route("/inquiries")
def list_inquiries():
    inquiries = Inquiry.query.all()
    return render_template("list_inquiries.html", inquiries=inquiries)

@views.route("/register", methods=["GET", "POST"])
def register():
    # Pokud je uživatel už přihlášen, přesměrujeme ho domů (volitelné)
    if current_user.is_authenticated:
        flash("Jste již přihlášen/a.", "info")
        return redirect(url_for("views.home"))

    if request.method == "POST":
        # 1) Načteme data z formuláře
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # 2) Základní validace - Kontrola shody hesel
        if password != confirm_password:
            flash("Hesla se neshodují!", "error")
            return redirect(url_for("views.register"))
        
        # 3) Ověřit, zda už neexistuje uživatel s daným e-mailem
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("E-mail je již používán. Zvolte jiný.", "error")
            return redirect(url_for("views.register"))

        # 4) Vytvoření nového uživatele
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # 5) (Volitelné) Hned přihlásit nového uživatele
        login_user(new_user)
        flash("Registrace proběhla úspěšně. Nyní jste přihlášen/a.", "success")
        
        # 6) Přesměrovat na homepage (nebo kam chcete)
        return redirect(url_for("views.home"))

    # GET request => zobrazíme šablonu
    return render_template("register.html")

@views.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            # heslo sedí
            login_user(user)
            flash("Přihlášení úspěšné!", "success")
            return redirect(url_for("views.home"))
        else:
            flash("Neplatné přihlašovací údaje!", "error")

    return render_template("login.html")

@views.route("/logout")
@login_required
def logout():
    """Odhlásí uživatele a přesměruje ho na homepage."""
    logout_user()  # Flask-Login funkce, zruší session pro daného uživatele
    flash("Byl jste úspěšně odhlášen.", "info")
    return redirect(url_for("views.home"))


@cart.route("/add", methods=["POST"])
@login_required
def add_to_cart():
    """Přidá produkt do košíku (nebo zvýší množství)"""
    data = request.get_json()
    product_id = data.get("product_id")

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Produkt nenalezen"}), 404

    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()

    if cart_item:
        cart_item.quantity += 1  # Zvýší množství
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)

    db.session.commit()
    return jsonify({"message": "Produkt přidán do košíku"}), 200

@cart.route("/remove", methods=["POST"])
@login_required
def remove_from_cart():
    """Odebere produkt z košíku"""
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
    """Vrátí obsah košíku pro přihlášeného uživatele"""
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
