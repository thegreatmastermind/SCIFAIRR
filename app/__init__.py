from flask import Flask
from .extensions import db
from .models import User
from flask_login import LoginManager
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "ayana"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    migrate = Migrate(app, db)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))   
    
    app.config['DEBUG'] = True 
    return app
