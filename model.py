"""Models for concert app"""
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return f'User: user_id={self.user_id} email={self.email}'

class Concert(db.Model):
    """A concert."""

    __tablename__ = "concerts"

    concert_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    band_name = db.Column(db.String)
    genre = db.Column(db.String)
    date = db.Column(db.DateTime)
    venue = db.Column(db.String)
    location = db.Column(db.String)
    band_pic_path = db.Column(db.String)

    user = db.relationship("User", backref="concerts")

    def __repr__(self):
        return f'Concert: concert_id={self.concert_id} band={self.band_name}'

def connect_to_db(flask_app, db_uri=os.environ["POSTGRES_URI"], echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Now connected to database")

if __name__ == "__main__":
    from server import app
    connect_to_db(app)