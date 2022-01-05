"""Automatically drop, recreate, and populate database"""

import os
import json
from random import choice, randint 
from datetime import datetime
import crud
import model
import server

os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

# Load movie data from JSON file
with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

# Create movies, store them in list so we can use them
# to create fake ratings later
movies_in_db = []
for movie in movie_data:    

    rd = datetime.strptime(movie["release_date"],"%Y-%m-%d")

    movie_to_add = crud.create_movie(
        title = movie["title"], 
        overview = movie["overview"], 
        release_date = rd, 
        poster_path = movie["poster_path"])

    movies_in_db.append(movie_to_add)

for n in range(10):
    email = f'user{n}@test.com'  # Voila! A unique email!
    password = 'test'

    user = crud.create_user(email=email, password=password)

    for i in range(10):
        crud.create_rating(user=user, movie=choice(movies_in_db), score=randint(1,5))

