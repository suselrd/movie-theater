# Movie Theater API

**Note:** As per requirements, there is no need for user roles separation, so the API can be consumed by anonymous users.

We have:

* Rooms with a specific number of seats (each)
* Movies that are playing
* Showtimes (a movie playing in a specific room at a specific date and time)
* Tickets to attend specific showtimes

## Simplified model

In order to make things easier we have assumed:

* Single currency: all prices are in the same currency, so only a decimal field is used for them.
* No Tax: all prices are "after-tax" prices.
* All seats available for a showtime have the same price (no VIP seats, or anything like it)


Also, there is no real payment when "buying" tickets.

## Installation

The solution uses Python 3.6.

1. Create a new virtualenv and **activate it**.
2. Install the requirements:

        $ pip install -r <path_to_project_directory>/requirements.txt


## Configuration (local settings)

If you are going to use a Postgres server running on localhost, you will need to set the following environment variables:

        SECRET_KEY=<secret_key_here>
        POSTGRES_USER=<user>
        POSTGRES_PASSWORD=<pass>

Alternatively, if you want to use a different database backend, o use a Postgres server running on a different host, you can:

1. Create a file local.py under <path/to/project/directory>/main/settings.
2. Set the value for the following setting:

        DATABASES = {
            'defult': {
                'ENGINE': 'django.db.backends.postgresql',
                'HOST': <host>,
                'NAME': <database_name>,
                'USER': <user>,
                'PASSWORD': <pass>,
                'PORT': <port>,
            }
        }

## Security

By default Cross-origin resource sharing (CORS) is only allowed for requests coming from APP_DOMAIN setting's value:
These are the involved settings:

    CORS_ORIGIN_ALLOW_ALL = False
    CORS_ORIGIN_REGEX_WHITELIST = (
        r'^(\w+?://)?127.0.0.1(:\d{1,5})?$',
        r'^(\w+?://)?localhost(:\d{1,5})?$',
        r'^(\w+?://)?%s$' % re.escape(APP_DOMAIN),
    )

The only thing we need to do then, is to set the proper value to the following environment variable:

    APP_DOMAIN=<domain_here>

To change that behavior, we have to update CORS_ORIGIN_REGEX_WHITELIST setting (Add another regex to the tuple, for instance).
We can do this by creating a local.py file and setting a new value to that setting there.

## Running
To run and test the API:

1. Make sure that your virtual environment is activated
2. Run:
    python manage.py runserver --settings=main.settings.compiled
3. You should see something like:

        Watching for file changes with StatReloader
        Performing system checks...

        System check identified no issues (0 silenced).
        June 20, 2020 - 17:28:31
        Django version 2.2.13, using settings 'main.settings.compiled'
        Starting development server at http://127.0.0.1:8000/
        Quit the server with CONTROL-C.

4. API is accessible at http://127.0.0.1:8000/api

## Interacting with the API

1. If you use a browser to access the API, a browsable, human friendly format will be served.
2. If you want to access the API programmatically just make sure to ask for the proper format by adding the following querystring argument:

        ?format=json


## How to create rooms

Make a POST request to http://127.0.0.1:8000/api/rooms/ with the following json content:

    {
        "name": "<room name>",
        "capacity": <number of seats, integer>
    }


## How to create movies

Make a POST request to http://127.0.0.1:8000/api/movies/ with the following json content:

    {
        "title": "<movie title>",
        "duration": <duration in minutes>
    }


## How to create movie showtimes

Make a POST request to http://127.0.0.1:8000/api/showtimes/ with the following json content:

    {
        "room": <room id>,
        "movie": <movie id>,
        "start": <datetime>,
        "price": <price of the ticket, decimal value>
    }

**Note** start datetime should follow the format: "Sat, 27 Jun 2020 01:30:00 PM"
Example content:

    {
        "room": 1,
        "movie": 1,
        "start": "Sat, 27 Jun 2020 01:30:00 PM",
        "price": "15.00"
    }

Showtime **end** datetime will be calculated automatically, using movie **duration** value.


## How to buy tickets

Make a POST request to http://127.0.0.1:8000/api/bookings/ with the following json content:

    {
        "showtime": <showtime id>,
        "seats": <number of seats / tickets>
    }

## What is playing in all the rooms?

Make a GET request to http://127.0.0.1:8000/api/rooms/. The result will include all the rooms in the theater,
including any current or upcoming showtimes they might have. Example response:

    {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "url": "http://127.0.0.1:8000/api/rooms/1/",
                "pk": 1,
                "name": "A",
                "capacity": 50,
                "upcoming_showtimes": [
                    {
                        "movie": "La vie est belle",
                        "start": "Fri, 26 Jun 2020 02:00:00 PM",
                        "price": "15.00",
                        "is_playing": false
                    },
                    {
                        "movie": "La vie est belle",
                        "start": "Sat, 27 Jun 2020 01:30:00 PM",
                        "price": "15.00",
                        "is_playing": false
                    }
                ]
            }
        ]
    }

## List of all the movies playing in the theater

Make a GET request to http://127.0.0.1:8000/api/movies/. The result will include all the movies playing in the theater.
Example response:

    {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "url": "http://127.0.0.1:8000/api/movies/1/",
                "pk": 1,
                "title": "La vie est belle",
                "duration": 120
            }
        ]
    }


## Other features

The API allows also to:

* see detailed information for a single room, movie or showtime (GET request to endpoint with url <list_url>/<id>/)
* update rooms, movies and showtimes (PUT requests to endpoint with url <list_url>/<id>/)
* delete rooms, movies and showtimes (DELETE requests to endpoint with url <list_url>/<id>/)


## Testing

Unit tests are written using **pytest**

To run the test suite and generate coverage report (in the terminal and in an html page):

    pytest -v --cov rooms --cov movies --cov schedule --cov tickets --cov-report term --cov-report html

**Note**: If you are using a virtualenv make sure it is active
