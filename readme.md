# Media Reviewer

This is a website for users to post reviews on their favourite media such as video games and movies
---

## Table of Contents:

* [UX](#ux-user-experience)
    * [Design Choices](#design-choices)
        * [Fonts](#fonts)
        * [Colours](#colours)
    * [Wireframes](#wireframe-mockups)
* [User Stories](#user-stories)git
* [Future Goals](#future-goals)
* [Project Planning](#project-planning)
* [Technology Used](#technologies-used)
* [Testing](#testing)
* [Issues](#issues)
    * [Open Issues](#open-issues)
    * [Closed Issues](#closed-issues)
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

## Credits

### Data
The data for this project was gotten from the following websites:


### Media
The photos used in this site were obtained from:
https://wallpaper-house.com/data/out/10/wallpaper2you_420670.jpg
https://mdbootstrap.com/docs/jquery/components/jumbotron/
https://elements.envato.com/movie-or-film-background-J7FLNA8
https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi1.wp.com%2Finfinite-av.com%2Fwp-content%2Fuploads%2F2018%2F03%2FTV-Icon.png&f=1&nofb=1

### Acknowledgements
I received inspiration for the design of the website from:
https://www.metacritic.com/
https://mdbootstrap.com/docs/jquery/navigation/footer/
https://mdbootstrap.com/docs/jquery/components/jumbotron/

I used the following websites for reseach:
* https://getbootstrap.com/docs/4.0/layout/media-object/
* https://bootstrapious.com/snippets
* https://speckyboy.com/css-content-cards/
* https://bootstrapious.com/p/circular-progress-bar
* https://getbootstrap.com/docs/4.0/components/collapse/
* https://www.youtube.com/watch?v=UIJKdCIEXUQ
* https://www.youtube.com/watch?v=J9O0v-iM0TE
* https://startbootstrap.com/snippets/full-image-header/

Images:
* https://elements.envato.com/heap-of-retro-tv-sets-with-no-signal-communication-PT4MC8R

Data for films was taken from:
https://www.imdb.com/

Data for video games was taken from:
https://www.metacritic.com/

All trailers were taken from:
https://www.youtube.com/

### Attribution
