# Twitter Parser

This is a small coding exercise about how to collect twitter posts containing specific keywords.

## Prerequisits

- Docker
- docker-compose
- Python 3.7

## Preliminary steps

Edit the `.env` file and enter the values for these fields:

- `USER_ID`
- `GROUP_ID`
- `TWITTER_APP_TOKEN`
- `TWITTER_APP_SECRET`

Make sure the values for `USER_ID` and `GROUP_ID` match your non-root user.
`TWITTER_APP_TOKEN` and `TWITTER_APP_SECRET` must be set to the values for the application you have registered in your twitter "dev account".

## Installation (initialize Database)

	$ ./scripts/init.py

## Running the Parser

	$ docker-compose up

## Stopping the Parser

	$ docker-compose down

## Cleaning the Database

	$ docker-compose down
	$ rm -r runtime_data
