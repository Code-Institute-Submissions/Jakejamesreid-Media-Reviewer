import os
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET")
app.config['DEBUG'] = True

MONGODB_URI = os.environ.get("MONGO_URI")
DBS_NAME = os.environ.get("DBS_NAME")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME")

game_posts = [
    {"title": "Game Post 1",
    "author": "John",
    "date": "20-01-2020",
    "content": "First Post"},

    {"title": "Game Post 2",
    "author": "Bob",
    "date": "12-05-2020",
    "content": "Second Post"},
]

movie_posts = [
    {"title": "Movie Post 1",
    "author": "John",
    "date": "20-01-2020",
    "content": "First Post"},

    {"title": "Movie Post 2",
    "author": "Bob",
    "date": "12-05-2020",
    "content": "Second Post"},
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/game-listings")
def game_listings():
    return render_template("game-listings.html", posts = game_posts, category="Games")

@app.route("/movie-listings")
def movie_listings():
    return render_template("movie-listings.html", posts = movie_posts, category="Movies")

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=os.environ.get("PORT"), debug=True)