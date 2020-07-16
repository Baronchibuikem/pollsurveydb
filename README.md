# Project Title

## Poll Vote Web Project


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

Make migrations, createsuperuser and run the server

    python manage.py makemigrations account polls
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver


### Built With

    Python - Programming language used
    Django-rest-framework - The web framework used
    django-rest-swagger - Used to generate documentation for all the endpoints

Contributing
Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

### Authors

Baron Chibuikem (A fullstack software developer)

### Acknowledgments

Regards to everyone whose contributed in the development of this project.