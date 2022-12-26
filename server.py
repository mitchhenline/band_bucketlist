"""Server for concert app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key= "kilby"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def homepage():
    """view homepage."""


    return render_template('homepage.html')

@app.route('/concerts/<user_id>')
def see_concerts(user_id):
    """view seen concert list."""

    user = crud.get_user_by_id(user_id)

    return render_template('concerts.html', user = user)

@app.route('/bucketlist/<user_id>')
def see_future_concerts(user_id):
    """view bucket list."""

    user = crud.get_user_by_id(user_id)

    return render_template('bucketlist.html', user = user)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)