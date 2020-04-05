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
- Activate the virtualenv `source .venv/bin/activate`
    - Windows: `cd .venv/Scripts` and `activate`, then `cd ../..`
- Install dependencies with pip `pip install -r requirements.txt`

## Setup application locally

- Run local postgres: `docker run -d -p 5432:5432 --name postgres -e POSTGRES_HOST_AUTH_METHOD=trust postgres`
- Run migrations `python vochabular/manage.py migrate`
- Run server `python vochabular/manage.py runserver`
- Create admin user `python vochabular/manage.py createsuperuser`

## Run application in docker

- Install docker and docker-compose
- Build or download and run images `docker-compose up -d`
- To setup the database (run the applicable migrations) and setup the Django superuser, first connect to the shell of the container: `
- Make sure to run the Django migrations to setup the DB: `docker exec -it vocha_admin_backend python manage.py migrate`
- Make sure to create the super user: `docker exec -it vocha_admin_backend python manage.py createsuperuser`

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
