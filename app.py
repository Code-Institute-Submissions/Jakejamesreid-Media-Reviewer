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

mongo = PyMongo(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/game-listings")
def game_listings():

    game_posts = list(mongo.db.games.find())
    # Determine the average user rating for each game
    game_posts_with_rating = calculateMediaRating(game_posts)

    return render_template("listings.html", posts = game_posts_with_rating, category="Games")

@app.route("/movie-listings")
def movie_listings():
    movie_posts = list(mongo.db.movies.find())
    movie_posts_with_rating = calculateMediaRating(movie_posts)
    return render_template("listings.html", posts = movie_posts_with_rating, category="Movies")

@app.route("/games/<media>", methods=["GET", "POST"])
def game_media(media):
    game = mongo.db.games.find_one({'name': media})
    form = SubmitReviewForm()
    game_with_rating = calculateMediaRating([game])

    if form.validate_on_submit():
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
        game = mongo.db.games.find_one({'name': media})
        game_with_rating = calculateMediaRating([game])
        flash("Review has been successfully submitted", "success")
        return redirect(url_for('game_media', media=game_with_rating[0]['name']))

    return render_template("media.html", media = game_with_rating[0], category="Games", form=form)

def calculateMediaRating(media_posts):
    """Return media posts for the given collection

    :param string collection: The name of the databases collection
    :return: List of media posts
    :rtype: list
    """
    for media in media_posts:
        overall_rating = 0
        for rating in media['review']:
            overall_rating+=int(rating['rating'])
        media['overall_rating'] = int(overall_rating/len(media['review']))

    return media_posts

# @app.route("/games/<media>/submit-review")
# def review(media):
#     form = SubmitReviewForm()
#     return render_template("review.html", media = game, form=form)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=os.environ.get("PORT"), debug=True)