# Twitter Parser

This is a small coding exercise about how to collect twitter posts containing specific keywords.

## Prerequisits

- Docker
- docker-compose
- Python 3.7

## Preliminary steps

Edit the `.env` file and make sure the values for `USER_ID` and `GROUP_ID` match your non-root user.

## Installation (initialize Database)

	$ ./scripts/init.py

## Running the Parser

	$ docker-compose up

## Stopping the Parser

	$ docker-compose down

## Cleaning the Database

	$ docker-compose down
	$ rm -r runtime_data
