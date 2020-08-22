import os
import requests
from datetime import datetime, date, timedelta
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import SubmitReviewForm, SortRatingForm, SearchMediaForm

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


def calculate_ratings_for_media(media_post):
    """Calculate the user rating for a given media post

    :param string media_post: The media that is to have its user rating calculated
    :return: Media post with user rating
    :rtype: dict
    """
    total_rating = 0

    for review in media_post['reviews']:
        total_rating += float(review['rating'])
    media_post['user_rating'] = round(
        total_rating/len(media_post['reviews']), 1)
    return media_post


def media_sort(media_posts, form, category):
    """Return sorted media posts for the given collection

    :param list media_posts: List of media posts
    :param form form: The sort by rating form
    :param string category: The collection to be sorted
    :return: List of media posts
    :rtype: list
    """
    if form.validate_on_submit():
        if form.rating.data == "1":
            media_posts = sorted(
                media_posts, key=lambda k: k['our_rating'], reverse=True)
        elif form.rating.data == "2":
            media_posts = sorted(media_posts, key=lambda k: k['our_rating'])

    return media_posts


def search_IGDB(body):
    """Queries the IGDB API for video games

    :param str body: search query to be used in the data parameter of the request
    :return: List of video games
    :rtype: list
    """
    gameRequest = requests.get('https://api-v3.igdb.com/games/',
                               headers={
                                   "user-key": IGDB_API
                               },
                               data=body)
    gameResults = gameRequest.json()
    return gameResults


def refactor_game_data(games):
    """Takes video games returned from IGDB and formats them correctly

    :param list games: Games returned from the IGDB API
    :return: List of video games in correct format
    :rtype: list
    """
    game_posts = []
    for game in games:
        if "name" not in game.keys():
            game['name'] = "Unknown Title"

        if "cover" in game.keys():
            # Change image url from thumbnail to cover image
            game['cover'] = game['cover']['url'].replace(
                "t_thumb", "t_cover_big")
        else:
            game['cover'] = 'static/img/placeholder.png'

        if "first_release_date" in game.keys():
            # Convert timestamp in ms to human readable date
            game['first_release_date'] = datetime.fromtimestamp(
                (game['first_release_date'])).strftime('%Y-%b-%d')
        else:
            game['first_release_date'] = "Unknown"

        game['supported_platforms'] = []
        if "platforms" in game.keys():
            # Get the abbreviations of the supported platforms for each game
            for i, platform in enumerate(game['platforms']):
                if "abbreviation" in platform.keys():
                    game['supported_platforms'].append(
                        platform['abbreviation'])
        else:
            game['supported_platforms'] = "Platforms Unknown"

        if "rating" not in game.keys():
            game['rating'] = 0

        if "summary" not in game.keys():
            game['summary'] = "No overview available for this title."

        if "genres" in game.keys():
            game['genres'] = game['genres'][0]['name']
        else:
            game['genres'] = "N/A"

        game['trailer'] = ""
        if "videos" in game.keys():
            # Use first YouTube video ID in list unless 'Trailer' video is available
            game['trailer'] = "https://www.youtube.com/embed/" + \
                game['videos'][0]['video_id']
            for video in game['videos']:
                if "Trailer" in video['name']:
                    game['trailer'] = "https://www.youtube.com/embed/" + \
                        video['video_id']
        else:
            game['videos'] = "N/A"

        game_posts.append(
            {
                "igdb_id": game['id'],
                "name": game['name'],
                "image_url": game['cover'],
                "release_date": game['first_release_date'],
                "our_rating": int(game['rating']),
                "platforms": ' '.join(game['supported_platforms']),
                "summary": game['summary'],
                "genre": game['genres'],
                "trailer": game['trailer']
            }
        )

    return game_posts
