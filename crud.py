"""CRUD operations."""
from model import db, User, Concert, connect_to_db

def create_user(email, password):
    user = User(email=email,password=password)
    return user

def create_concert(band_name, genre, date, venue, location, band_pic_path, user):
    concert = Concert(
        band_name=band_name, 
        genre=genre,
        date=date,
        venue=venue,
        location=location,
        band_pic_path=band_pic_path,
        user=user)
    return concert

def get_user_by_id(user_id):
    return User.query.get(user_id)

if __name__ == '__main__':
    from server import app
    connect_to_db(app)