import os
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import SubmitReviewForm
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
if os.path.exists(__location__+"\\env.py"):
    import env

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config['DEBUG'] = True

def calculateMediaRating(collection):
    """Return media posts for the gicen collection

    :param string collection: The name of the databases collection
    :return: List of media posts
    :rtype: list
    """
    mongo = PyMongo(app)
    media_posts = list(mongo.db[collection].find())
    for media in media_posts:
        overall_rating = 0
        for rating in media['review']:
            overall_rating+=rating['rating']
        media['overall_rating'] = overall_rating/len(media['review'])
        mongo.db[collection].update_one({'name': media['name']},{'$set':{'overall_rating': media['overall_rating']}})

    return media_posts

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/game-listings")
def game_listings():

    # Determine the average user rating for each game
    game_posts = calculateMediaRating("games")

    return render_template("listings.html", posts = game_posts, category="Games")

@app.route("/movie-listings")
def movie_listings():
    movie_posts = calculateMediaRating("movies")
    return render_template("listings.html", posts = movie_posts, category="Movies")

@app.route("/games/<media>", methods=["GET", "POST"])
def game_media(media):
    mongo = PyMongo(app)
    game = mongo.db.games.find_one({'name': media})
    
    form = SubmitReviewForm()
    if form.validate_on_submit():
        flash("Review has been successfully submitted", "success")
        mongo = PyMongo(app)
        
        mongo.db["games"].update_one(
            {'name': media},
            {
                '$push':
                {
                    'review': 
                    {
                        "id": ObjectId(),
                        "author": form.name.data,
                        "comment": form.comment.data,
                        "rating": form.rating.data,
                        "date_uploaded": datetime.now()
                    }
                }
            })

    return render_template("media.html", media = game, category="Games", form=form)

# @app.route("/games/<media>/submit-review")
# def review(media):
#     form = SubmitReviewForm()
#     return render_template("review.html", media = game, form=form)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=os.environ.get("PORT"), debug=True)