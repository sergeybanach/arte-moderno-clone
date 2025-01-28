class Config:
    SECRET_KEY = 'arte_moderno'  # Váš tajný klíč
    SQLALCHEMY_DATABASE_URI = 'sqlite:///arte_moderno.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Nastavení pro Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'  # Gmail SMTP
    MAIL_PORT = 587                 # TLS port
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'artemodernoblaha@gmail.com'  # Váš e-mail (např. GMail)
    MAIL_PASSWORD = 'qxunfbtnyvefainm' 
    # POZOR: pro GMail musíte často použít tzv. "App Password" ve 2FA
    # Nebo musíte povolit "méně bezpečné aplikace" (nedoporučuje se!)
