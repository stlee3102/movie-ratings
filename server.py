"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session, redirect, url_for)
from model import connect_to_db
import crud
from flask_sqlalchemy import SQLAlchemy

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

    user = crud.get_user_by_id(session['user'])
    movie_ratings = movie.ratings

    total_score = 0
    for ratings in movie.ratings:
        total_score += ratings.score
    if total_score == 0:
        avg_rating = 'Not yet rated'
    else:
        avg_rating = f'{total_score/len(movie.ratings)} stars'

    return render_template('movie_details.html', movie=movie, movie_ratings=movie_ratings, user=user, avg_rating=avg_rating)

@app.route("/rate_movie/<movie_id>", methods=["POST"])
def rate_movie(movie_id):
    """Create a new movie rating"""

    movie = crud.get_movie_by_id(movie_id)
    score = request.form.get("score")
    rating_user = crud.get_user_by_id(session['user'])

    if crud.get_rating_by_movie_by_user(movie, rating_user):
        crud.update_rating(rating_user, movie, score)
    else:
        crud.create_rating(rating_user, movie, score)
  
    return redirect(f'/movies/{movie_id}')

@app.route('/users')
def show_all_users():

    list_users = crud.return_all_users()

    return render_template('users.html', list_users=list_users)

@app.route('/users', methods=["POST"])
def register_user():
    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)

    if user:
        flash("User already created")
    else:
        crud.create_user(email, password)
        flash("Account registered")
    return redirect("/")


@app.route('/login', methods=["POST"])
def login_user():

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        if password == user.password:
            session['user'] = user.user_id
            flash(f"logged in {user.user_id} {user.email} {user.password}")
        else:
            flash("incorrect password, try again")
    else:
        flash("user not registered")

    return redirect("/")

@app.route('/users/<user_id>')
def show_user(user_id):

    user = crud.get_user_by_id(user_id)

    return render_template('user_details.html', user=user)


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
