# admin-backend

This is the backend of the admin interface, used internally [@Vochabular](https://www.vochabular.ch) for the creation, translation, reviewing and publishing of content.

## Introduction

This is a python django application providing a GraphQL API to the SPA. It uses Graphene for GraphQL and PyJWT for JWT authentication.

## How to install

- Install python3 and virtualenv
- Create a virtualenv in the checkout: `virtualenv -p python3 .venv`
- Activate the virtualenv `source .venv/bin/activate`
    - Windows: `cd .venv/Scripts` and `activate`, then `cd ../..`
- Install dependencies with pip `pip install -r requirements.txt`

## Setup application

- Run migrations `python vochabular/manage.py migrate`
- Run server `python vochabular/manage.py runserver`
- Create admin user `python vochabular/manage.py createsuperuser`

## Run application in docker

- Install docker and docker-compose
- Build or download and run images `docker-compose up -d`

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
