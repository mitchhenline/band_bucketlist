"""CRUD operations."""
from model import db, User, Concert, connect_to_db, BucketList
from forms import AddConcert

def create_user(email, password):
    user = User(email=email,password=password)
    return user
        

def create_future_concert(band_name, genre, band_pic_path, user):
    concert = Concert(
        band_name=band_name, 
        genre=genre,
        band_pic_path=band_pic_path,
        user=user)
    return concert

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_email(email) -> User:
    return User.query.filter(User.email == email).first()

def get_concerts(email: str):
    user = get_user_by_email(email)
    return Concert.query.filter(Concert.user_id == user.user_id)

def get_bucket_list(email: str):
    user = get_user_by_email(email)
    return BucketList.query.filter(BucketList.user_id == user.user_id)

def get_concert_by_id(concert_id):
    return Concert.query.get(concert_id)


if __name__ == '__main__':
    from server import app
    connect_to_db(app)