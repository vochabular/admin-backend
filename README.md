# admin-backend

This is the backend of the admin interface, used internally [@Vochabular](https://www.vochabular.ch) for the creation, translation, reviewing and publishing of content.

## Introduction

The backend consists of two API applications that are connected to Postgres:

### A python Django Application for model classes and business logic

- Mainly used for central business logic such as presigning S3 uploads
- Has Model classes (Code first) definitions to automatically create necessary db migrations
- Uses Graphene to serve a GraphQL API endpoint
- Uses PyJWT for JWT authentication

### Hasura GraphQL engine
- A stateless service running on top of postgres
- Automatically provides a GraphQL schema based on the underlaying Postgres DB
- Used for boring CRUD operations and so called `subscriptions` (live queries via websockets)
- Used for the ACL of CRUD operations
- Consumes the Django GraphQL schema and merges into one to serve the clients a single schema

## How to install

- Install python3 and virtualenv
- Create a virtualenv in the checkout: `virtualenv -p python3 .venv`
- Activate the virtualenv `source .venv/bin/activate && pip install pip-tools`
    - Windows: `cd .venv/Scripts` and `activate`, then `cd ../..`
- Install dependencies with pip `pip install -r requirements.txt`

## Change dependencies

We use [pip-tools](https://github.com/jazzband/pip-tools) for dependency management. To add a new
package, add it to `requirements.in` and run `pip-compile`, followed by `pip-sync`.
To upgrade all dependencies, run `pip-compile --upgrade` and `pip-sync`.

## Setup application locally

- Run local postgres: `docker run -d -p 5432:5432 --name postgres -e POSTGRES_HOST_AUTH_METHOD=trust postgres`
- Run migrations `python vochabular/manage.py migrate`
- Run server `python vochabular/manage.py runserver`
- Create admin user `python vochabular/manage.py createsuperuser`

## Run application in docker

- Install docker and docker-compose
- Build or download and run images `docker-compose up -d`
- Make sure to run the Django migrations to setup the DB: `docker exec -it vocha_admin_backend python manage.py migrate`
- Make sure to create the super user: `docker exec -it vocha_admin_backend python manage.py createsuperuser`

## Sync staging database with local psql database
With `heroku pg:pull`and `heroku pg:push` you either pull the postgresql database from heroku to your local machine or push your local database to heroku:

`heroku pg:pull DATABASE vochabular --app vochabular-admin`

This command creates a new local database named `vochabular` and then pulls data from the database at `DATABASE` from the app `vochabular-admin`. To prevent accidental data overwrites and loss, the local database must not already exist. You will be prompted to drop an already existing local database before proceeding.

If providing a Postgres user or password for your local DB is necessary, use the appropriate environment variables like so:

`PGUSER=postgres PGPASSWORD=password heroku pg:pull DATABASE vochabular --app vochabular-admin`


`pg:push` pushes data from a local database into a remote Heroku Postgres database. The command looks like this:

`heroku pg:push mylocaldb DATABASE --app vochabular-admin`

This command takes the local database `mylocaldb` and pushes it to the database at `DATABASE` on the app `vochabular-admin`. To prevent accidental data overwrites and loss, the remote database must be empty. You will be prompted to `pg:reset` a remote database that is not empty.

Usage of the PGUSER and PGPASSWORD for your local database is also supported for `pg:push`, just like for the `pg:pull` command.

## Sample GraphQL Queries

```
query {
  chapters {
    titleDE,
    text
  }
}
```

```
mutation {
  createChapter(input: {chapterData: {titleCH: "title CH", titleDE: "title DE", text: "asdf"}}) {
    chapter{
      titleCH,
      text
    }
  }
}
```
