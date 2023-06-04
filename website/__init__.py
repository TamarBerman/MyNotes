from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db"

manager = {
    'email':'tamar3242643@gmail.com',
    'password':'1234567890',
}


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hi my final project tamar berman'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Note

    with app.app_context():
        db.create_all()

    # create_database(app)

    # בכניסה לאתר ישר פונה ללוגין
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # אומר לפלאסק איך לטעון יוזר
    @login_manager.user_loader
    def laod_user(id):
        return User.query.get(int(id))

    return app


def create_database(myapp):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=myapp)
        print("Created DB")
