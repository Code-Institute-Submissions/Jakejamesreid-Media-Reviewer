import os
from flask import Flask, render_template, request, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
if os.path.exists(__location__+"\\env.py"):
    import env

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config['DEBUG'] = True

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/game-listings")
def game_listings():
    mongo = PyMongo(app)
    game_posts = list(mongo.db.games.find())

    # Determine the average user rating for each game
    for game in game_posts:
        overall_rating = 0
        for rating in game['review']:
            overall_rating+=int(rating['rating'])
        game['overall_rating'] = overall_rating/len(game['review'])

    return render_template("listings.html", posts = game_posts, category="Games")

@app.route("/movie-listings")
def movie_listings():
    return render_template("listings.html", posts = movie_posts, category="Movies")

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=os.environ.get("PORT"), debug=True)