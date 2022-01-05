"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = StrictUndefined


# Replace this with routes and view functions!

@app.route('/')
def homepage():
    """ view homepage """

    return render_template('homepage.html')

@app.route('/movies')
def show_all_movies():

    list_movies = crud.return_all_movies()

    return render_template('movies.html', list_movies=list_movies)

@app.route('/movies/<movie_id>')
def show_movie(movie_id):

    movie = crud.get_movie_by_id(movie_id)

    return render_template('movie_details.html', movie=movie)

@app.route('/users')
def show_all_users():

    list_users = crud.return_all_users()

    return render_template('users.html', list_users=list_users)

@app.route('/users/<user_id>')
def show_user(user_id):

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
