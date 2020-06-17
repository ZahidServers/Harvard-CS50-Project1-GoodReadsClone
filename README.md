# Project 1

Web Programming with Python and JavaScript
---
## Fixture
Fixed API doesnt redirect 404.html if page is not it now sends back an json response in application.py
---
youtube Link Here https://youtu.be/aXd_a5sTLRY
---
youtube screencast here:https://www.youtube.com/watch?v=Ff5oheI9Z88
---
## Features
### This project Contains Following Features-
---
Template page with header, searchbar, sticky navbar and footer
---
A home page visible to all guest and users that change it self dynamically after login
---
A Search system that gives both users and guest ability to search for books from Database
---
A book page that fetch all the details about book and ratings and reviews allows user to post his review and give it stars out of 5 for rating and a textrea to add review about book it allows each user only to review once the user post it he is again redericted to same book page where he can view his post and ratings.The unloginned users are automatically redirected to login page and if a book page does not exist it redirects to custom 404.html page
---
A login/Registration system if any guest tries to visit book page or api he is sended to login page login registration page are interlinked with each other futhermore if a user tries to login with wrong password he is displayed an error message on login page itself.
If a new user registers sucessfully he is redirected to login page with message being displayed as Account Succesfully Created Now Login.
---
API logined users can send api request using book isbn no and they get a json response back if the user enters wrongg isbn he will be automatically redirected to 404.html error page.
---
## Pages
### there are following pages:-
---
import.py : Creates TABLES and imports csv file and insert data from csv into books table
---
application.py is the main file that runs flasks web app it contains all the python code
---
static folder contains all the image files
---
Template folder contains all the pages used
---
template.html is the template displayed to loginned users
---
template2.html is the template displayed to guests
---
search.html is used for search with template.html for loginned users it displays search results
---
search2.html is used for guest extending template2.html it displays search results
---
book.html displays book information title author year and it allows users to make reviews and give ratings and after submitting store their review in db and displays them their revies through Database
---
index.html is the home page for loginned users
---
index2.html is the home page for guests
---
login.html for logging in
---
registar.html for registration onto site
---
404.html for displaying Page Not Found errors rest errors are displayed with the pages itself for example login displays invalid credentials at login page itself simmilarly search displays search results not found
---
api.json Displays the json response and if response not found displays error code
---
