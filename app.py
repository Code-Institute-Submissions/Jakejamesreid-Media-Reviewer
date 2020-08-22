from functions import *


@app.route("/")
def index():

    one_year_ago = int((datetime.now() - timedelta(days=365) - datetime(1970,1,1)).total_seconds())
    search_query = f"""fields name,cover.url,first_release_date,rating,platforms.abbreviation;
    where first_release_date > {one_year_ago};
    sort popularity desc;
    limit 4;"""
    popular_games = search_IGDB(search_query)
    popular_games_refactored = refactor_game_data(popular_games)

    movie_posts = list(mongo.db.movies.find())
    return render_template("index.html", game_posts = popular_games_refactored, movie_posts = movie_posts[:4])

@app.route("/game-listings", methods=["GET", "POST"])
def game_listings():

    # # Check if user searched for a game
    search_media_form = SearchMediaForm()

    if request.method == 'POST':
        game_searched_by_user  = request.form.get('search')
        if game_searched_by_user:
            search_query = f"""fields name,cover.url,first_release_date,rating,platforms.abbreviation;
                    search "{game_searched_by_user}";
                    limit 20;"""
            IGDB_games = search_IGDB(search_query)
            if IGDB_games:
                IGDB_games = refactor_game_data(IGDB_games)

                # Sort posts by rating
                sort_by_rating_form = SortRatingForm()
                sorted_game_posts = media_sort(IGDB_games, sort_by_rating_form, "Games")
                return render_template("listings.html", posts = sorted_game_posts, category="Games", rating_form=sort_by_rating_form, media_form = search_media_form)

    one_year_ago = int((datetime.now() - timedelta(days=365) - datetime(1970,1,1)).total_seconds())
    search_query = f"""fields name,cover.url,first_release_date,rating,platforms.abbreviation;
    where first_release_date > {one_year_ago};
    sort popularity desc;
    limit 20;"""
    most_popular_games = search_IGDB(search_query)

    if most_popular_games:
        game_posts = refactor_game_data(most_popular_games)

    # Sort posts by rating
    sort_by_rating_form = SortRatingForm()
    sorted_game_posts = media_sort(game_posts, sort_by_rating_form, "Games")

    return render_template("listings.html", posts = sorted_game_posts, category="Games", rating_form=sort_by_rating_form, media_form = search_media_form)


@app.route("/movie-listings",  methods=["GET", "POST"])
def movie_listings():
    media_posts = list(mongo.db.movies.find())
    rating_form = SortRatingForm()
    sorted_movies = media_sort(media_posts, rating_form, "Movies")
    
    return render_template("listings.html", posts = sorted_movies, category="Movies", rating_form=rating_form)
    
@app.route("/games/<igdb_id>", methods=["GET", "POST"])
def game_media(igdb_id):

    userReviewForm = SubmitReviewForm()

    search_query = f"""fields name,cover.url,first_release_date,rating,platforms.abbreviation,summary,genres.name,videos.*;
    where id = {igdb_id};"""
    IGDB_game = search_IGDB(search_query)
    IGDB_game_refactored = refactor_game_data(IGDB_game)[0]

    # Check for user review
    user_reviews = mongo.db.games.find_one({'igdb_id': str(IGDB_game_refactored['igdb_id'])})

    if user_reviews:
        user_reviews_with_rating = calculate_ratings_for_media(user_reviews)
        IGDB_game_refactored['reviews'] = user_reviews_with_rating['reviews']
        IGDB_game_refactored['reviews'] = user_reviews_with_rating['reviews']
        IGDB_game_refactored['user_rating'] = user_reviews_with_rating['user_rating']

        # Check if user submitted a review
        if userReviewForm.validate_on_submit():
                # Update the database with user review
            mongo.db.games.update_one(
            {'igdb_id': igdb_id},
            {
                '$push':
                {
                    'reviews': 
                    {
                        "id": ObjectId(),
                        "author": userReviewForm.name.data,
                        "comment": userReviewForm.comment.data,
                        "rating": userReviewForm.rating.data,
                        "date_uploaded": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                }
            })
            flash("Review has been successfully submitted", "success")
            return redirect(url_for('game_media', igdb_id=igdb_id))
        return render_template("game_details.html", media = IGDB_game_refactored, category="Games", form=userReviewForm)
    
    # If no reviews on page
    else:
        # Check if user submitted a review
        if userReviewForm.validate_on_submit():
            # Update the database with user review
            mongo.db.games.insert(
                {
                    'igdb_id': igdb_id,
                    'reviews': [
                    {
                        "id": ObjectId(),
                        "author": userReviewForm.name.data,
                        "comment": userReviewForm.comment.data,
                        "rating": userReviewForm.rating.data,
                        "date_uploaded": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }]
                })

            flash("Review has been successfully submitted", "success")
            return redirect(url_for('game_media', igdb_id=igdb_id))
        return render_template("game_details.html", media = IGDB_game_refactored, category="Games", form=userReviewForm)

@app.route("/movies/<media>", methods=["GET", "POST"])
def movie_media(media):
    movie = mongo.db.movies.find_one({'name': media})
    movie_with_rating = calculate_ratings_for_media(movie)
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
        
        flash("Review has been successfully submitted", "success")
        return redirect(url_for('movie_media', media=movie_with_rating['name']))

    return render_template("media.html", media = movie_with_rating, category="Movies", form=form)

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"), port=os.environ.get("PORT"), debug=True)
