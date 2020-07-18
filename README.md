## Project Title

### Poll Vote Web Project

This web project is aimed at allowing user's of the platform submit a poll(question and choices) and other users can vote on their 
preferred choice. at the end of the poll duration the poll creator can use the result of the poll to make informed decisions etc.

This is the server side Api's for this project, the client side can be seen in the following repo <https://github.com/Baronchibuikem/YouChooseFrontend>

### Functionalities implemented

    1. User Authentication
    2. Poll and Choice creation
    3. Bookmarking of polls
    4. Liking of polls
    5. Following of users
    6. Unfollowing of users
    7. Updating of polls and choices
    8. Deleting of polls and choices
    9. Deleting of likes and bookmarks

### Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

    Python 3.6.9

### Installing

You'll need to have a virtual environment installed on your machine

    pip3 install virtualenv

Setup virtual environment

    virtualenv -p python3.6 .virtualenv

Activate virtual environment

    source .virtualenv/bin/activate

Install the requirements

    pip install -r requirements

Go to the folder youchooseDjango/settings and comment out the production_settings and uncomment the development settings so you can use the development setting to run this project locally on your machine

Make migrations, createsuperuser and run the server

    python manage.py makemigrations account polls
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

### Built With

    Python - Programming language used
    Django-rest-framework - The web framework used
    django-rest-swagger - Used to generate documentation for all the endpoints

### Important notes

The media files are being served through cloudinary, you will need to setup a cloudinary account if you dont have one, but if you do, the create a .env file in the root of this project and add the following

    CLOUD_NAME = "your cloud name"
    API_KEY = "your api key"
    API_SECRET = "your secret key"

### Authors

Baron Chibuikem (A fullstack software developer)

### Acknowledgments

Regards to everyone whose contributed in the development of this project.