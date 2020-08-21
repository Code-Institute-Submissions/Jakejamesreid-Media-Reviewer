from functions import *


@app.route("/")
def index():

    # Get the latest Video Games and Movies
    game_posts = list(mongo.db.games.find())
    movie_posts = list(mongo.db.movies.find())

    return render_template("index.html", game_posts = game_posts[:4], movie_posts = movie_posts[:4])


@app.route("/game-listings", methods=["GET", "POST"])
def game_listings():

    game_posts = []

    # Check if user searched for a game
    search_media_form = SearchMediaForm()
    game_search_keyword = check_if_game_search_performed()

    if game_search_keyword:
        game_results = mongo.db.games.find_one({'name': game_search_keyword})
        if game_results:
            return redirect(url_for('game_media', igdb_id=game_results['igdb_id']))
        else:                
            game_results = search_IGDB(game_search_keyword)
            if game_results:
                    
                for game in game_results:
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
    game_posts_with_rating = calculate_ratings_for_media(game_posts)

    # Determine the average user rating for each game
    rating_form = SortRatingForm()
    sorted_game_posts = media_sort(game_posts_with_rating, rating_form)

    return render_template("listings.html", posts = sorted_game_posts, category="Games", rating_form=rating_form, media_form = media_form)


@app.route("/movie-listings",  methods=["GET", "POST"])
def movie_listings():
    media_posts = list(mongo.db.movies.find())
    media_posts_with_rating = calculate_ratings_for_media(media_posts)
    rating_form = SortRatingForm()
    sorted_game_movie_with_rating = media_sort(movie_posts, rating_form)
    
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
            game = calculate_ratings_for_media([game])

            flash("Review has been successfully submitted", "success")
            return redirect(url_for('game_media', igdb_id=game[0]['igdb_id']))

        game = calculate_ratings_for_media([game])
        return render_template("media.html", media = game[0], category="Games", form=userReviewForm)
    else:
        game_request = requests.get('https://api-v3.igdb.com/games/', 
        headers={
            "user-key": IGDB_API
        },
        data=f"""fields name,cover.*,platforms.*;
                        where id =  {igdb_id};""")
        game = game_request.json()
        if game:
            pass
            # add_new_game_to_DB(game)
        return redirect(url_for('game_media', igdb_id=game['igdb_id']))

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