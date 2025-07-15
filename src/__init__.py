
# It initializes the Flask application and sets up the database connection.
from flasgger import Swagger
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # SQLAlchemy instance
DB_NAME = "students"  # Optional use if needed later

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'vishal_key'
    
    # Postgres URI (URL-encoded special characters)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:vishal%4011@localhost:5433/students'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    Swagger(app)

    return app
