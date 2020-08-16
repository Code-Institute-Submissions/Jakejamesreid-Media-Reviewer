# Media Reviewer

This is a website for users to post reviews on their favourite media such as video games, movies and TV Shows
---

## Table of Contents:

* [UX](#ux-user-experience)
    * [Design Choices](#design-choices)
        * [Fonts](#fonts)
        * [Colours](#colours)
    * [Wireframes](#wireframe-mockups)
* [User Stories](#user-stories)
* [Features](#features)
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


### Design Choices

#### Fonts


#### Colours


### Wireframe Mockups


---

## User stories
Below is a list if the specific user stories for this project.


---

## Features


---

## Future Goals


---

## Project Planning

---

## Technologies Used

* HTML 
* CSS 
* JavaScript 
* [Bootstrap](https://getbootstrap.com/) - to help adapt for numerous input types
* [VSCode](https://code.visualstudio.com/) - IDE for local development
* [GIT](https://git-scm.com/) - Version Control
* [Heroku](https://heroku.com) - to host the project
* [JQuery](https://jquery.com) - Used to simplify Javascript
* [FontAwesome](https://fontawesome.com/) - Used for icons
---


## Testing

---

## Issues

### Open Issues
The list below displays the current **open** issues with the project:

1. If invalid range is specified for the rating field on the review form and the user hits submit, the page will reload and the user will have to scroll back down to the form to see the error message. Ideally the page would not reload

### Closed Issues

The list below displays the current **closed** issues with the project:

1. Database displayed stale data after submitting a review. The solution was to make another call to read the database after updating it with new data.
2. After submitting the review form thjere was an issue where when the page was refreshed the form would be submitted again. The solution for this was to add a redirect to the same page in the game_media route as opposed to using render_template. Redirecting allows the page to get a fresh state where as with render_template the browser was storing the state from the last request.
3. A very unexpected error was that Jinja seems to read Jinja commands even when they are commented out. The following line was still being processed by Jinja in a HTML file. 
"""
<!-- {{ render_field(form.rating) }} -->
"""
---

## Credits

### Data
The data for this project was gotten from the following websites:


### Media
The photos used in this site were obtained from:

### Acknowledgements
I received inspiration for the design of the website from:
https://www.metacritic.com/

I used the following websites for reseach:
* https://getbootstrap.com/docs/4.0/layout/media-object/
* https://bootstrapious.com/snippets
* https://speckyboy.com/css-content-cards/
* https://bootstrapious.com/p/circular-progress-bar
* https://getbootstrap.com/docs/4.0/components/collapse/
* https://www.youtube.com/watch?v=UIJKdCIEXUQ
* https://www.youtube.com/watch?v=J9O0v-iM0TE

Data for films was taken from:
https://www.imdb.com/

Data for video games was taken from:
https://www.metacritic.com/

All trailers were taken from:
https://www.youtube.com/
### Attribution
