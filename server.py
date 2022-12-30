"""Server for concert app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db, User, Concert
import crud
from jinja2 import StrictUndefined
from forms import LoginForm, AddConcert
from crud import add_concert

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
        flash('Logged in.')
        return redirect('/')

    return render_template("login.html", form=form)

@app.route('/logout')
def logout():

    del session['email']
    flash("Logged out.")
    return redirect("/login")

@app.route('/concerts')
def see_concerts():
    """view seen concert list."""

    if 'email' not in session:
        return redirect('/login')

    concerts = crud.get_concerts(session["email"])
    form = AddConcert(request.form)

    if form.validate_on_submit():
        band_name = form.band_name.data
        date = form.date.data
        venue = form.venue.data
        location = form.location.data
        band_pic_path = form.band_pic_path.data

    return render_template('concerts.html', concerts = concerts, form=form)

# @app.route("/add_concert", methods=["POST"])
# def add_concert():

#     new_concert = crud.add_concert()




@app.route('/bucketlist')
def see_future_concerts():
    """view bucket list."""
    if 'email' not in session:
        return redirect('/login')


    return render_template('bucketlist.html')

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)