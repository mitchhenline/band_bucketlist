"""Server for concert app."""

from flask import Flask, render_template, request, flash, session, redirect, abort
from model import connect_to_db, db, User, Concert, BucketList
import crud
from jinja2 import StrictUndefined
from forms import LoginForm, AddConcert, AddBucketList
from crud import get_user_by_email, get_concert_by_id

app = Flask(__name__)
app.secret_key= "kilby"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """view homepage."""
    if 'email' not in session:
        return redirect('/login')


    return render_template('homepage.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    """log user into site"""
    form = LoginForm(request.form)

    # Form is submitted with valid data
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

    #Check to see if a user with this email exists
        user = crud.get_user_by_email(email)
        if not user or user.password != password:
            flash("Invalid email or password")
            return redirect('/login')

        session['email'] = user.email
        return redirect('/')

    return render_template("login.html", form=form)

@app.route('/logout')
def logout():

    del session['email']
    flash("Logged out.")
    return redirect("/login")

@app.route('/concerts', methods=["GET"])
def see_concerts():
    """view seen concert list."""
    form = AddConcert(request.form)
    if 'email' not in session:
        flash("Please log in")
        return redirect('/login')
    concerts = crud.get_concerts(session["email"])
    return render_template('concerts.html', concerts = concerts, form=form)

@app.route('/concerts', methods=["POST"])
def post_concert():
    form = AddConcert(request.form)
    if 'email' not in session:
        return redirect('/login')
    if form.validate_on_submit():
        concert = Concert(
            band_name = form.band_name.data,
            date = form.date.data,
            genre = form.genre.data,
            venue = form.venue.data,
            location = form.location.data,
            band_pic_path = form.band_pic_path.data,
            user_id = get_user_by_email(session["email"]).user_id
        )
        db.session.add(concert)
        db.session.commit()
        return redirect("/concerts")
    else:
        abort(404)

@app.route('/concerts/<concert_id>')
def show_concert(concert_id):
    """Show details of a concert."""
    if 'email' not in session:
        return redirect('/login')
    concert = crud.get_concert_by_id(concert_id)

    return render_template("see_concert.html", concert = concert)

@app.route('/concerts/<concert_id>/delete')
def delete_concert(concert_id):
    """Delete concert."""
    if 'email' not in session:
        return redirect('/login')

    concert = crud.get_concert_by_id(concert_id)
    db.session.delete(concert)
    db.session.commit()

    return redirect('/concerts')

@app.route('/bucketlist', methods=["GET"])
def see_future_concerts():
    """view bucket list."""
    form = AddBucketList(request.form)
    if 'email' not in session:
        flash("Please log in")
        return redirect('/login')
    bucket_list = crud.get_bucket_list(session["email"])
    return render_template('bucketlist.html', bucket_list = bucket_list, form = form)

@app.route('/bucketlist', methods=["POST"])
def post_future_concert():
    form = AddBucketList(request.form)
    if 'email' not in session:
        return redirect('/login')
    if form.validate_on_submit():
        bucket_list = BucketList(
            band_name = form.band_name.data,
            genre = form.genre.data,
            band_pic_path = form.band_pic_path.data,
            user_id = get_user_by_email(session["email"]).user_id
        )
        db.session.add(bucket_list)
        db.session.commit()
        return redirect("/bucketlist")
    else:
        abort(404)

@app.route('/bucketlist/<future_concert_id>')
def show_future_concert(future_concert_id):
    """Show details of a concert."""

    if 'email' not in session:
        return redirect('/login')

    future_concert = crud.get_future_concert_by_id(future_concert_id)

    return render_template("see_future_concert.html", future_concert = future_concert)

@app.route('/bucketlist/<future_concert_id>/delete')
def delete_future_concert(future_concert_id):
    """Delete future concert."""
    if 'email' not in session:
        return redirect('/login')

    future_concert = crud.get_future_concert_by_id(future_concert_id)
    db.session.delete(future_concert)
    db.session.commit()

    return redirect('/bucketlist')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)