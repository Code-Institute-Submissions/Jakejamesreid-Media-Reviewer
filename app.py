from functions import *


@app.route("/")
def index():

    # Get the latest Video Games and Movies
    game_posts = list(mongo.db.games.find())
    movie_posts = list(mongo.db.movies.find())
    return render_template("index.html", game_posts = game_posts[:4], movie_posts = movie_posts[:4])

@app.route("/game-listings", methods=["GET", "POST"])
def game_listings():

    # # Check if user searched for a game
    search_media_form = SearchMediaForm()
    game_searched_by_user = check_if_game_search_performed()

    if game_searched_by_user:
        search_query = f"""fields name,cover.url,first_release_date,rating,platforms.abbreviation;
                search "{game_searched_by_user}";
                limit 20;"""
        IGDB_games = search_IGDB(search_query)
        if IGDB_games:
            IGDB_games = refactor_game_data(IGDB_games)

            # Sort posts by rating
            rating_form = SortRatingForm()
            sorted_game_posts = media_sort(IGDB_games, rating_form, "Games")
            return render_template("listings.html", posts = sorted_game_posts, category="Games", rating_form=rating_form, media_form = search_media_form)

    one_year_ago = int((datetime.now() - timedelta(days=365) - datetime(1970,1,1)).total_seconds())
    search_query = f"""fields name,cover.url,first_release_date,rating,platforms.abbreviation;
    where first_release_date > {one_year_ago};
    sort popularity desc;
    limit 20;"""
    most_popular_games = search_IGDB(search_query)

    if most_popular_games:
        game_posts = refactor_game_data(most_popular_games)

    # Sort posts by rating
    rating_form = SortRatingForm()
    sorted_game_posts = media_sort(game_posts, rating_form, "Games")

    return render_template("listings.html", posts = sorted_game_posts, category="Games", rating_form=rating_form, media_form = search_media_form)


@app.route("/movie-listings",  methods=["GET", "POST"])
def movie_listings():
    media_posts = list(mongo.db.movies.find())
    media_posts_with_rating = calculate_ratings_for_media(media_posts)
    rating_form = SortRatingForm()
    sorted_movie_with_rating = media_sort(media_posts_with_rating, rating_form, "Movies")
    
    return render_template("listings.html", posts = sorted_movie_with_rating, category="Movies", rating_form=rating_form)
    
@app.route("/games/<igdb_id>", methods=["GET", "POST"])
def game_media(igdb_id):

    search_query = f"""fields name,cover.url,first_release_date,rating,platforms.abbreviation,summary,genres.name,videos.*;
    where id = {igdb_id};"""
    IGDB_game = search_IGDB(search_query)
    IGDB_game[0]['reviews'] = []

    game = refactor_game_data(IGDB_game)

    DB_game = mongo.db.games.find_one({'igdb_id': str(IGDB_game[0]['id'])})
    if DB_game:
        game[0]['reviews'] = DB_game['reviews']
    userReviewForm = SubmitReviewForm()

    return render_template("game_details.html", media = game[0], category="Games", form=userReviewForm)
    # game = mongo.db.games.find_one({'igdb_id': igdb_id})
    # if game:
    #     # Check if user submitted a review
    #     userReviewForm = SubmitReviewForm()
    #     if userReviewForm.validate_on_submit():
    #         # Update the database with user review
    #         mongo.db["games"].update_one(
    #         {'igdb_id': igdb_id},
    #         {
    #             '$push':
    #             {
    #                 'review': 
    #                 {
    #                     "id": ObjectId(),
    #                     "author": userReviewForm.name.data,
    #                     "comment": userReviewForm.comment.data,
    #                     "rating": userReviewForm.rating.data,
    #                     "date_uploaded": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #                 }
    #             }
    #         })

    #         # Get the latest data from the database and calculate the new rating
    #         game = mongo.db.games.find_one({'igdb_id': igdb_id})
    #         game = calculate_ratings_for_media([game])

    #         flash("Review has been successfully submitted", "success")
    #         return redirect(url_for('game_media', igdb_id=game[0]['igdb_id']))

    #     game = calculate_ratings_for_media([game])
    #     return render_template("media.html", media = game[0], category="Games", form=userReviewForm)
    # else:
    #     game_request = requests.get('https://api-v3.igdb.com/games/', 
    #     headers={
    #         "user-key": IGDB_API
    #     },
    #     data=f"""fields name,cover.*,platforms.*;
    #                     where id =  {igdb_id};""")
    #     game = game_request.json()
    #     if game:
    #         pass
    #         # add_new_game_to_DB(game)
    #     return redirect(url_for('game_media', igdb_id=game['igdb_id']))

@app.route("/movies/<media>", methods=["GET", "POST"])
def movie_media(media):
    movie = mongo.db.movies.find_one({'name': media})
    form = SubmitReviewForm()

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
        movie_with_rating = mongo.db.movies.find_one({'name': media})
        flash("Review has been successfully submitted", "success")
        return redirect(url_for('movie_media', media=movie_with_rating['name']))

    movie_with_rating = mongo.db.movies.find_one({'name': media})
    return render_template("media.html", media = movie_with_rating, category="Movies", form=form)

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=os.environ.get("PORT"), debug=True)
