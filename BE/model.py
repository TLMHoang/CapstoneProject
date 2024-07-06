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
class Product(db.Model): 
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    # Relationship with Posts
    posts = db.relationship("Serial", backref="author", uselist=False, lazy=True)

    def __init__(self, name):
        self.name = name

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name
            }

# Post model
class Serial(db.Model):
    __tablename__ = 'serials'

    id = db.Column(db.Integer, primary_key=True)
    imei = db.Column(db.String(200), nullable=False)

    # Foreign key to User
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    def __init__(self, imei, product_id):
        self.imei = imei
        self.product_id = product_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'imei': self.imei,
            'product_id': self.product_id
        }