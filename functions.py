import os
import requests
from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import SubmitReviewForm, SortRatingForm, SearchMediaForm

from functions import *
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
if os.path.exists(__location__+"\\env.py"):
    import env

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
IGDB_API = os.environ.get("IGDB_API")
app.config['DEBUG'] = True

mongo = PyMongo(app)

def get_media_with_ratings(media_type):
    media_posts = list(mongo.db[media_type].find())
    media_posts_with_rating = calculate_ratings_for_media(media_posts)
    return media_posts

def calculate_ratings_for_media(media_post):
    """Calculate the user rating for a given media post

    :param string media_post: The media that is to have its user rating calculated
    :return: Media post with user rating
    :rtype: dict
    """
    total_rating = 0

    # Calculate for single post
    for review in media_post['reviews']:
        total_rating+=float(review['rating'])
    media_post['user_rating'] = round(total_rating/len(media_post['reviews']), 1)
    return media_post

def media_sort(media_posts, form, category):
    """Return media posts for the given collection

    :param string collection: The name of the databases collection
    :return: List of media posts
    :rtype: list
    """
    # Sort posts by rating
    if form.validate_on_submit():
        if category == "Games":
            if form.rating.data == "1":
                media_posts = sorted(media_posts, key=lambda k: k['our_rating'], reverse=True) 
            elif form.rating.data == "2":
                media_posts = sorted(media_posts, key=lambda k: k['our_rating']) 
        elif category == "Movies":
            if form.rating.data == "1":
                media_posts = sorted(media_posts, key=lambda k: k['overall_rating'], reverse=True) 
            elif form.rating.data == "2":
                media_posts = sorted(media_posts, key=lambda k: k['overall_rating']) 

    return media_posts

def check_if_game_search_performed():
    """
    Checks if the user search form has been filled out
    """
    if request.method == 'POST':
        search_result  = request.form.get('search')
        if search_result:
            return search_result
        else:
            return False
        
def search_IGDB(body):
    gameRequest = requests.get('https://api-v3.igdb.com/games/', 
    headers={
        "user-key": IGDB_API
    },
    data=body)
    gameResults = gameRequest.json()
    return gameResults

def add_new_game_to_DB(game):

    if "cover" in game.keys():
        game['cover']['url'].replace("t_thumb", "t_cover_big")
    else:
        game['cover'] = {'url':'static/img/placeholder.png'}

    if "first_release_date" in game.keys():
        game['first_release_date'] = datetime.fromtimestamp((game['first_release_date'])).strftime('%Y-%b-%d')
    else:
        game['first_release_date'] = "Unknown"

    if "platforms" in game.keys():
        game['platforms'] = game['platforms']['abbreviation']
    else:
        game['platforms'] = "Unknown"

    mongo.db["games"].insert(
        {
        'igdb_id': game['id'],
        'name': game['name'],
        'image_url': game['name'],
        'video_url': game['name'],
        'description': game['name'],
        'media_category': game['platforms'],
        'release_date': game['name'],
        'developer': game['name'],
        'review': [],
        'overall_rating': game['name'],
        }
        )


def refactor_game_data(games):
 
    game_posts = []
    for index,game in enumerate(games):
        if "name" not in game.keys():
            game['name'] = "Unknown Title"

        if "cover" in game.keys():
            game['cover'] = game['cover']['url'].replace("t_thumb", "t_cover_big")
        else:
            game['cover'] = {'url':'static/img/placeholder.png'}

        if "first_release_date" in game.keys():
            game['first_release_date'] = datetime.fromtimestamp((game['first_release_date'])).strftime('%Y-%b-%d')
        else:
            game['first_release_date'] = "Unknown"
        
        game['supported_platforms'] = []
        if "platforms" in game.keys():
            for platform in game['platforms']:
                if "abbreviation" in platform.keys():
                    game['supported_platforms'].append(platform['abbreviation'])
        else:
            game['supported_platforms'] = "Platforms Unknown"

        if "rating" in game.keys():
            game['rating'] = int(game['rating'])
        else:
            game['rating'] = 0

        if "summary" not in game.keys():
            game['summary'] = "No overview available for this title."

        if "genres" in game.keys():
            game['genres'] = game['genres'][index]['name']
        else:
            game['genres'] = "N/A"

        game['trailer'] = ""
        if "videos" in game.keys():
            game['trailer'] = game['videos'][0]['video_id']
            for video in game['videos']:
                if "Trailer" in video['name']:
                    game['trailer'] = "https://www.youtube.com/embed/"+video['video_id']


        else:
            game['videos'] = "N/A"

        game_posts.append(
            {
                "igdb_id": game['id'], 
                "name": game['name'], 
                "image_url": game['cover'],
                "release_date": game['first_release_date'],
                "our_rating": game['rating'],
                "platforms": ' '.join(game['supported_platforms']),
                "summary": game['summary'],
                "genre": game['genres'],
                "trailer": game['trailer']
            }
        )

    return game_posts