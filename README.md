# Planbrothers Test Exercise

[![Travis-ci Build Status](https://travis-ci.org/Isabek/planbrothersapp.svg?branch=master)](https://travis-ci.org/Isabek/planbrothersapp)

## Creating DB on Postgres

```sh
$ psql -U postgres
postgres=# CREATE USER root WITH PASSWORD 'root';
postgres=#  CREATE DATABASE bro_db OWNER root;
```

## Running Locally

```sh
$ git clone git@github.com:Isabek/planbrothersapp.git
$ cd planbrothersapp
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

$ python manage.py db upgrade

$ python manage.py runserver
```

Your app should now be running on [localhost:5000](http://localhost:5000/).