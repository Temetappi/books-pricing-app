# Pricing app for books

## Requirements

Docker

Python 3.12

## Running the application

To run the application, run the following command in a terminal:

**docker compose up**

This will start the database(Postgresql) and the app itself in docker containers.
There is a also a pre-start migrate service that runs before the app, making sure
that the database is created and up to date with the latest migration.

Initial test data is created in one of the migrations.

The API is available at localhost:8080
Swagger is available at http://localhost:8080/docs
