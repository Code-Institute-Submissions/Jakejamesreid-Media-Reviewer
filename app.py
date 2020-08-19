import os
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import SubmitReviewForm, SortRating
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

@app.route("/game-listings", methods=["GET", "POST"])
def game_listings():

    game_posts = list(mongo.db.games.find())
    print('hello')
    rating_form = SortRating()
    # Determine the average user rating for each game
    game_posts_with_rating = calculateMediaRatingAndSort(game_posts, rating_form)

    return render_template("listings.html", posts = game_posts_with_rating, category="Games", rating_form=rating_form)

@app.route("/movie-listings",  methods=["GET", "POST"])
def movie_listings():
    movie_posts = list(mongo.db.movies.find())
    rating_form = SortRating()
    movie_posts_with_rating = calculateMediaRatingAndSort(movie_posts, rating_form)

    
    return render_template("listings.html", posts = movie_posts_with_rating, category="Movies", rating_form=rating_form)

@app.route("/games/<media>", methods=["GET", "POST"])
def game_media(media):
    game = mongo.db.games.find_one({'name': media})
    form = SubmitReviewForm()
    game_with_rating = calculateMediaRatingAndSort([game], form)

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
        game_with_rating = calculateMediaRatingAndSort([game], form)
        flash("Review has been successfully submitted", "success")
        return redirect(url_for('game_media', media=game_with_rating[0]['name']))

    return render_template("media.html", media = game_with_rating[0], category="Games", form=form)

@app.route("/movies/<media>", methods=["GET", "POST"])
def movie_media(media):
    movie = mongo.db.movies.find_one({'name': media})
    form = SubmitReviewForm()
    movie_with_rating = calculateMediaRatingAndSort([movie], form)

    if form.validate_on_submit():
        mongo.db["movies"].update_one(
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
        movie = mongo.db.games.find_one({'name': media})
        movie_with_rating = calculateMediaRatingAndSort([movie], form)
        flash("Review has been successfully submitted", "success")
        return redirect(url_for('movie_media', media=movie_with_rating[0]['name']))

    return render_template("media.html", media = movie_with_rating[0], category="Movies", form=form)

def calculateMediaRatingAndSort(media_posts, form):
    """Return media posts for the given collection

    :param string collection: The name of the databases collection
    :return: List of media posts
    :rtype: list
    """

    media_posts = list(reversed(media_posts))
    for media in media_posts:
        overall_rating = 0
        for rating in media['review']:
            overall_rating+=int(rating['rating'])
        media['overall_rating'] = int(overall_rating/len(media['review']))

    # Sort posts by rating
    if form.validate_on_submit():
        if form.rating.data == "1":
            media_posts = sorted(media_posts, key=lambda k: k['overall_rating'], reverse=True) 
        elif form.rating.data == "2":
            media_posts = sorted(media_posts, key=lambda k: k['overall_rating']) 
    return media_posts


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=os.environ.get("PORT"), debug=True)