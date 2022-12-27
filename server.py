"""Server for concert app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
from forms import LoginForm

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

        if not user or user['password'] != password:
            flash("Invalid email or password")
            return redirect('/login')

        session['username'] = user['username']
        flash('Logged in.')
        return redirect('/')

    return render_template("login.html", form=form)

@app.route('/concerts')
def see_concerts(user_id):
    """view seen concert list."""

    user = crud.get_user_by_id(user_id)

    return render_template('concerts.html', user = user)

@app.route('/bucketlist')
def see_future_concerts(user_id):
    """view bucket list."""

    user = crud.get_user_by_id(user_id)

    return render_template('bucketlist.html', user = user)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)