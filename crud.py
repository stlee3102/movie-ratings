"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def return_all_users():
    """Return all users"""
    return User.query.all()

def get_user_by_id(user_id):
    """Return user from user id"""

    return User.query.get(user_id)

def get_user_by_email(email):
    """Return user from email"""

    return User.query.filter(User.email == email).first()

def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""

    movie = Movie(title=title, overview=overview, release_date=release_date, poster_path=poster_path)

    db.session.add(movie)
    db.session.commit()

    return movie

def return_all_movies():
    """Return all movies"""
    return Movie.query.all()

def get_movie_by_id(movie_id):
    """Return movie description based on movie id"""

    return Movie.query.get(movie_id)

def create_rating(user, movie, score):
    """Create and return a new rating"""

    rating = Rating(user=user, movie=movie, score=score)
    db.session.add(rating)
    db.session.commit()

    return rating

def update_rating(user, movie, score):
    """Update rating"""

    Rating.query.filter(Rating.movie_id == movie.movie_id, Rating.user_id == user.user_id).update({"score": score})
    db.session.commit()

def get_rating_by_movie_by_user(movie, user):
    """Return a ratings for a movie by a user"""
    return Rating.query.filter_by(movie=movie, user=user).all()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)