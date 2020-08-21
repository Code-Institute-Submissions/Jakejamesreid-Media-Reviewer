import os
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import SubmitReviewForm, SortRatingForm, AddMediaForm
import requests
import env

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
IGDB_API = os.environ.get("IGDB_API")
app.config['DEBUG'] = True

mongo = PyMongo(app)

@app.route("/")
def index():
    game_posts = list(mongo.db.games.find())
    game_posts_with_rating = calculateMediaRating(game_posts)

    movie_posts = list(mongo.db.movies.find())
    movie_posts_with_rating = calculateMediaRating(movie_posts)

    return render_template("index.html", game_posts = game_posts_with_rating[:4], movie_posts = movie_posts[:4])


@app.route("/game-listings", methods=["GET", "POST"])
def game_listings():

    game_posts = []
    userSearch = checkForUserSearchForm()

    if userSearch:
        gameResults = mongo.db.games.find_one({'name': userSearch})
        if gameResults:
            return redirect(url_for('game_media', igdb_id=gameResults['igdb_id']))
        else:                
            gameResults = searchIGDB(userSearch)
            if gameResults:
                    
                for game in gameResults:
                    if "cover" in game.keys():
                        game['cover']['url'].replace("t_thumb", "t_cover_big")
                    else:
                        game['cover'] = {'url':'static/img/placeholder.png'}

                    if "first_release_date" in game.keys():
                        game['first_release_date'] = datetime.fromtimestamp((game['first_release_date'])).strftime('%Y-%b-%d')
                    else:
                        game['first_release_date'] = "Unknown"
                        
                    print(game)
                    game_posts.append(
                        {
                            "name": game['name'], 
                            "url": game['cover']['url'],
                            "release_date": game['first_release_date']
                        }
                    )
                    # print(game_posts)

                return render_template("search.html", posts = game_posts, category="Games")

    game_posts = list(mongo.db.games.find())
    rating_form = SortRatingForm()

    # Determine the average user rating for each game
    game_posts_with_rating = calculateMediaRating(game_posts)
    sorted_game_posts_with_rating = mediaSort(game_posts, rating_form)

    media_form = AddMediaForm()

    return render_template("listings.html", posts = sorted_game_posts_with_rating, category="Games", rating_form=rating_form, media_form = media_form)


@app.route("/movie-listings",  methods=["GET", "POST"])
def movie_listings():
    movie_posts = list(mongo.db.movies.find())
    rating_form = SortRatingForm()
    movie_posts_with_rating = calculateMediaRating(movie_posts)
    sorted_game_movie_with_rating = mediaSort(movie_posts, rating_form)
    
    return render_template("listings.html", posts = sorted_game_movie_with_rating, category="Movies", rating_form=rating_form)
    
@app.route("/games/<igdb_id>", methods=["GET", "POST"])
def game_media(igdb_id):

    game = mongo.db.games.find_one({'igdb_id': igdb_id})
    if game:
        # Check if user submitted a review
        userReviewForm = SubmitReviewForm()
        if userReviewForm.validate_on_submit():
            # Update the database with user review
            mongo.db["games"].update_one(
            {'igdb_id': igdb_id},
            {
                '$push':
                {
                    'review': 
                    {
                        "id": ObjectId(),
                        "author": userReviewForm.name.data,
                        "comment": userReviewForm.comment.data,
                        "rating": userReviewForm.rating.data,
                        "date_uploaded": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                }
            })

            # Get the latest data from the database and calculate the new rating
            game = mongo.db.games.find_one({'igdb_id': igdb_id})
            game = calculateMediaRating([game])

            flash("Review has been successfully submitted", "success")
            return redirect(url_for('game_media', igdb_id=game_with_rating[0]['igdb_id']))

        game = calculateMediaRating([game])
        return render_template("media.html", media = game[0], category="Games", form=userReviewForm)
    else:
        gameRequest = requests.get('https://api-v3.igdb.com/games/', 
        headers={
            "user-key": IGDB_API
        },
        data=f"""fields name,cover.*,platforms.*;
                        where id =  {igdb_id};""")
        game = gameRequest.json()
        if game:
            pass
            # addNewGameToDB(game)
        return redirect(url_for('game_media', igdb_id=game['igdb_id']))


# def addNewGameToDB(game):

#     if "cover" in game.keys():
#         game['cover']['url'].replace("t_thumb", "t_cover_big")
#     else:
#         game['cover'] = {'url':'static/img/placeholder.png'}

#     if "first_release_date" in game.keys():
#         game['first_release_date'] = datetime.fromtimestamp((game['first_release_date'])).strftime('%Y-%b-%d')
#     else:
#         game['first_release_date'] = "Unknown"

#     if "platforms" in game.keys():
#         game['platforms'] = game['platforms']['abbreviation']
#     else:
#         game['platforms'] = "Unknown"

#     mongo.db["games"].insert(
#         {
#         'igdb_id': game['id'],
#         'name': game['name'],
#         'image_url': game['name'],
#         'video_url': game['name'],
#         'description': game['name'],
#         'media_category': game['platforms'],
#         'release_date': game['name'],
#         'developer': game['name'],
#         'review': [],
#         'overall_rating': game['name'],
#         }
#         )

@app.route("/movies/<media>", methods=["GET", "POST"])
def movie_media(media):
    movie = mongo.db.movies.find_one({'name': media})
    form = SubmitReviewForm()
    movie_with_rating = calculateMediaRating([movie])

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
        movie_with_rating = calculateMediaRating([movie])
        flash("Review has been successfully submitted", "success")
        return redirect(url_for('movie_media', media=movie_with_rating[0]['name']))

    return render_template("media.html", media = movie_with_rating[0], category="Movies", form=form)


def calculateMediaRating(media_posts):
    """Return media posts for the given collection

    :param string collection: The name of the databases collection
    :return: List of media posts
    :rtype: list
    """

    media_posts = list(reversed(media_posts))
    for media in media_posts:
        overall_rating = 0
        for rating in media['review']:
            overall_rating+=float(rating['rating'])
        media['overall_rating'] =  round(overall_rating/len(media['review']), 1)

    return media_posts

def mediaSort(media_posts, form):
    """Return media posts for the given collection

    :param string collection: The name of the databases collection
    :return: List of media posts
    :rtype: list
    """
    # Sort posts by rating
    if form.validate_on_submit():
        if form.rating.data == "1":
            media_posts = sorted(media_posts, key=lambda k: k['overall_rating'], reverse=True) 
        elif form.rating.data == "2":
            media_posts = sorted(media_posts, key=lambda k: k['overall_rating']) 
    return media_posts

def checkForUserSearchForm():
    """
    Checks if the user search form has been filled out
    """
    if request.method == 'POST':
        search_result  = request.form.get('search')
        if search_result:
            return search_result
        else:
            return False
        
def searchIGDB(name):
    print(name)
    gameRequest = requests.get('https://api-v3.igdb.com/games/', 
    headers={
        "user-key": IGDB_API
    },
    data=f"""fields name,cover.url,first_release_date;
                    search "{name}";
                    limit 20;""")
    gameResults = gameRequest.json()
    return gameResults


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=os.environ.get("PORT"), debug=True)