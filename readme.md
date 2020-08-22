# Media Reviewer

This is a website for users to post reviews on their favourite media such as video games and movies. Other media types will be added in the future such as music, books, etc. So this will be an all in one review website for the user to review any type of media.
---

## Table of Contents:

* [UX](#ux-user-experience)
    * [Wireframes](#wireframe-mockups)
* [User Stories](#user-stories)
* [Future Goals](#future-goals)
* [Project Planning](#project-planning)
* [Technology Used](#technologies-used)
* [Testing](#testing)
* [Issues](#issues)
    * [Open Issues](#open-issues)
    * [Closed Issues](#closed-issues)
* [Deployment](#deployment)
* [Credits](#credits)

---

## UX (User Experience)

## Wireframe Mockups

## Homepage
<div style="text-align:center;">
    <img src="assets\img\Homepage.png"></img><br>
</div>

### Listings Page
<div style="text-align:center;">
    <img src="assets\img\Listing Page.png"></img><br>
</div>

### Media Details Page
<div style="text-align:center;">
    <img src="assets\img\Media Page.png"></img><br>
</div>

### Review Page
This page was not needed in the final version as the form for submitting a review was incorporated into the listings page.
<div style="text-align:center;">
    <img src="assets\img\Review Page.png"></img><br>
</div>
---

## User stories
Below is a list if the specific user stories for this project.
1. As a user I want to be able to submit a review for a specific video game.
2. As a user I want to be able to see the average rating a video game has received.
3. As a user I want to be able to submit a review for a specific movie.
4. As a user I want to be able to see the average rating a movie has received.
5. As a user I want to be able to search for a specific video game or movie.

---

## Future Goals

### Implement Other Media Types
The current solution only supports Video Games and Movies. This can be expanded to support other media types such as TV Shows, Music, Books, etc

### Dynamically changing colour for the Rating Bubble
The current rating bubble only displays a green colour. If a user gave a score of < 4 then the colour should be red and if the rating was > 4 and < 7 the colour should be orange. Green wuld then only be used for ratings of 7 or higher.

### User can edit or delete reviews
Currently the user can only post a review. In a future update the user would also be able to edit or delete their reviews.

### Implement API for movies
Thye current implementation only has an API for searching video games and not for movies. A future update would be to add this functionality to movies as well.

---

## Project Planning

**Stage 1** - Implement the template for listing the different media entries.

**Stage 2** - Implement the template for a specific media entry.

**Stage 3** - Populate the templates with data from the MongoDB database.

**Stage 4** - Allow users to add their own reviews to specific media entries and post the data to the Database.

**Stage 5** - Implement the homepage layoput.

**Stage 6** - Allow users to add a media entry to the database by submitting a form. This form should use an API to get all the details for the specific media that the user wants to add.

**Stage 7** - Improve the design and UX of the website.

**Stage 8** - Test robustness of the site and optimize performance and code.

---

## Technologies Used

* HTML 
* CSS 
* JavaScript 
* [Bootstrap](https://getbootstrap.com/) - to help adapt for numerous input types
* [MD Bootstrap](https://mdbootstrap.com/md-bootstrap-cdn/) - Used for enhabced bootstrap designs
* [VSCode](https://code.visualstudio.com/) - IDE for local development
* [GIT](https://git-scm.com/) - Version Control
* [Heroku](https://heroku.com) - to host the project
* [JQuery](https://jquery.com) - Used to simplify Javascript
* [FontAwesome](https://fontawesome.com/) - Used for icons
* [Google Fonts](https://fonts.googleapis.com/) - Used for fonts
---


## Testing

### Navagation Bar
1. Ensure that clicking the logo or the home button takes the user to the homepage
2. Ensure that clicking the games button takes the user to the game listings page
3. Ensure that clicking the games button takes the user to the movie listings page
4. Ensure that the menu is responsive


### Homepage Testing
Buttons:
1. Ensure that the button in the Games Jumbotron redirects the user to the games listing page.
2. Ensure that the buttons in the Movies Jumbotron redirect the user to the movie listing page.

Responsiveness:
1. Ensure that the games Jumbotron resizes to 2 games per row on small devices and 4 games on every other device.
2. Ensure that the movies Jumbotron resizes to 2 movies per row on small devices and 4 games on every other device.

### Game Listings Page Testing

Buttons:
1. Ensure that the sort button correctly sorts the games for Rating High to Low
2. Ensure that the sort button correctly sorts the games for Rating Low to High

Listing:
1. Ensure that clicking a games title redirects the user to the media_details page for that title
2. Ensure that clicking a games title redirects the user to the media_details page for that title after having sorted the games
3. Ensure that each listing displays the correct rating value
4. Ensure that the circular progress bar displays the correct colour based on rating value
5. Ensure that the Platforms being displayed for the game is correct
6. Ensure that the Release Date being displayed for the game is correct
7. Ensure that the Image being displayed for the game is correct

Search Bar:
1. Ensure that the search bar displays a list of games with similar names to what the user entered

### Movie Listings Page Testing

Buttons:
1. Ensure that the sort button correctly sorts the movies for Rating High to Low
2. Ensure that the sort button correctly sorts the movies for Rating Low to High

Listing:
1. Ensure that clicking a movies title redirects the user to the media_details page for that title
2. Ensure that clicking a movies title redirects the user to the media_details page for that title after having sorted the movies
3. Ensure that each listing displays the correct rating value
4. Ensure that the circular progress bar displays the correct colour based on rating value
5. Ensure that the Genres being displayed for the movie is correct
6. Ensure that the Release Date being displayed for the movie is correct
7. Ensure that the Image being displayed for the movie is correct

### Game Details Page Testing

Title:
1. ensure the correct title is displayed for the game

Video:
1. Ensure that the correct Youtube video is displayed for the game
2. Ensure that the Youtube video plays

Game Details Section:
1. Ensure that the Genre, Release Date, Our Rating and User Rating is correct for a given game
2. Ensure that each of these parameters display a fall back value when info is not available

Overview:
1. Ensure that the overview is displayed for a given game.
2. Ensure that the fallback value is displayed when info is not present

Buttons:
1. Ensure that the Add Review button toogles the visibility of the review form when pressed

Form:
1. Ensure that the form will not submit if all fields are empty and that an error message is displayed
2. Ensure that the form will not submit if the Name field is empty and that an error message is displayed
3. Ensure that the form will not submit if the Comment field is empty and that an error message is displayed
4. Ensure that the rating dropdown list displays values from 1-10
5. Ensure that the form submits the correct data to the database when the Submit Review button is pressed

Reviews:
1. Ensure that the correct quantity of reviews is being displayed for a given game
2. Ensure that the correct user review name, rating and comment is being displayed for a given game

### Movie Details Page Testing

Title:
1. ensure the correct title is displayed for the movie

Video:
1. Ensure that the correct Youtube video is displayed for the movie
2. Ensure that the Youtube video plays

movie Details Section:
1. Ensure that the Running Time, Our Rating and User Rating is correct for a given movie
2. Ensure that each of these parameters display a fall back value when info is not available

Overview:
1. Ensure that the overview is displayed for a given movie.
2. Ensure that the fallback value is displayed when info is not present

Buttons:
1. Ensure that the Add Review button toogles the visibility of the review form when pressed

Form:
1. Ensure that the form will not submit if all fields are empty and that an error message is displayed
2. Ensure that the form will not submit if the Name field is empty and that an error message is displayed
3. Ensure that the form will not submit if the Comment field is empty and that an error message is displayed
4. Ensure that the rating dropdown list displays values from 1-10
5. Ensure that the form submits the correct data to the database when the Submit Review button is pressed

Reviews:
1. Ensure that the correct quantity of reviews is being displayed for a given movie
2. Ensure that the correct user review name, rating and comment is being displayed for a given movie

---

## Issues

### Open Issues
The list below displays the current **open** issues with the project:


### Closed Issues

The list below displays the current **closed** issues with the project:

1. Database displayed stale data after submitting a review. The solution was to make another call to read the database after updating it with new data.
2. After submitting the review form thjere was an issue where when the page was refreshed the form would be submitted again. The solution for this was to add a redirect to the same page in the game_media route as opposed to using render_template. Redirecting allows the page to get a fresh state where as with render_template the browser was storing the state from the last request.
3. A very unexpected error was that Jinja seems to read Jinja commands even when they are commented out. The following line was still being processed by Jinja in a HTML file. 
4. If invalid range is specified for the rating field on the review form and the user hits submit, the page will reload and the user will have to scroll back down to the form to see the error message. The rating field now uses a dropdown menu so an invalid range cannot be selected.
"""
<!-- {{ render_field(form.rating) }} -->
"""
5. Rating bubble displays numbers with more than one decimal place. Used the round function in python to fix this

---

## Deployment

### Install the Heroku CLI
Download and install the Heroku CLI.
If you haven't already, log in to your Heroku account and follow the prompts to create a new SSH public key.
$ heroku login

### Create a new Git repository
Initialize a git repository in a new or existing directory
```
$ cd my-project/
$ git init
$ heroku git:remote -a {project-name}
```

### Create a requirements.txt file
This file contains a list of dependencies. We use this to tell Heroku that we will be using Python in our code.
pip3 freeze --local > requirements.txt

### Create a Procfile
A procfile is a special kind of file that tells Heroku how to run our project. (VS code needs to be in UTF-8 otherwise push will fail.)
Create a new file in the project root called Procfile and enter the following text
```
web: python app.py
```

### Final Production setup
Add environment variables in Heroku. Navigate to the settings tab in Heroku Dashboard and click "Config Vars".
Environment variables used are:
* MONGO_URI - URI for MongoDB
* SECRET - Secret key to encrypt data
* IGDB_API - API for IGDB
* PORT - Port Used
* IP - Default IP

### Push to Heroku
```
git add .
git commit -m "Added Requirements and Procfile" 
git push -u heroku master
```

### Final set up for Heroku
Start a web process by entering the following into the Heroku CLI
```
heroku ps:scale web=1
```

View the logs by navigating to "More->View logs"

Then go to "More->Restart all dynos" to restart the application. Everything should now be up and running


### Set up virtual environment
Flask is a web development server for Python. Open a admin terminal
1. Cd to project directory and install a virtual environment
```
pip install virtualenv
```
2. Create a virtual environment 
```
python -m venv env
```
3. Change the pythion interpreter in VS Code to be the python file located inside the venv

---

## Credits

### Data
The data for this project was gotten from the following websites:
* https://www.imdb.com/
* https://www.igdb.com/
* https://www.youtube.com/
* https://elements.envato.com/heap-of-retro-tv-sets-with-no-signal-communication-PT4MC8R

### Media
The photos used in this site were obtained from:
* https://wallpaper-house.com/data/out/10/wallpaper2you_420670.jpg
* https://elements.envato.com/movie-or-film-background-J7FLNA8
* https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi1.wp.com%2Finfinite-av.com%2Fwp-content%2Fuploads%2F2018%2F03%2FTV-Icon.png&f=1&nofb=1

### Acknowledgements
I received inspiration for the design of the website from:
* https://www.metacritic.com/
* https://mdbootstrap.com/docs/jquery/navigation/footer/
* https://mdbootstrap.com/docs/jquery/components/jumbotron/

I used the following websites for reseach:
* https://getbootstrap.com/docs/4.0/layout/media-object/
* https://bootstrapious.com/snippets
* https://speckyboy.com/css-content-cards/
* https://bootstrapious.com/p/circular-progress-bar
* https://getbootstrap.com/docs/4.0/components/collapse/
* https://www.youtube.com/watch?v=UIJKdCIEXUQ
* https://www.youtube.com/watch?v=J9O0v-iM0TE
* https://startbootstrap.com/snippets/full-image-header/

### Attribution
A special thanks to my mentor Akshat Garg for his help and advice during this project.