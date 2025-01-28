from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Inquiry
from app import db, mail  # importujeme db a mail z __init__.py
from flask_mail import Message

views = Blueprint("views", __name__)

@views.route("/", methods=["GET"])
def home():
    return render_template("home.html")  # jen příklad

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
