from datetime import datetime
import os
from flask_migrate import Migrate
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy_utils import database_exists, create_database
# from flask_moment import Moment


db = SQLAlchemy()

def setup_db(app, database_path):
    with app.app_context():
        engine = create_engine(database_path)

        if not database_exists(engine.url):  # Check if the database exists
            create_database(engine.url)     # Create it if it doesn't

        app.config["SQLALCHEMY_DATABASE_URI"] = database_path
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.app = app
        db.init_app(app)
        db.create_all()
    # db = SQLAlchemy(app)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# User model
class User(db.Model): 
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    token = db.Column(db.String(1024), nullable=False) 
    registration_date = db.Column(db.DateTime)
    role = db.Column(db.String(20), default='reader')

    # Relationship with Posts
    posts = db.relationship("Post", backref="author", uselist=False, lazy=True)

# Post model
class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    publication_date = db.Column(db.DateTime)
    slug = db.Column(db.String(200), unique=True, nullable=False)

    # Foreign key to User
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)