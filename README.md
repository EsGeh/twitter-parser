# Twitter Parser

This is a small coding exercise about how to collect twitter posts containing specific keywords.

## Prerequisits

- Docker
- docker-compose
- Python 3.7
- gradle

## Preliminary steps

	$ cp .env.def .env

Edit the `.env` file and enter the values for these fields:

- `USER_ID`
- `GROUP_ID`
- `TWITTER_APP_TOKEN`
- `TWITTER_APP_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_SECRET`

Make sure the values for `USER_ID` and `GROUP_ID` match your non-root user.
`TWITTER_APP_TOKEN`, `TWITTER_APP_SECRET`, `TWITTER_ACCESS_TOKEN` and `TWITTER_ACCESS_SECRET` must be set to the values for the application you have registered in your twitter "dev account".

## Installation (initialize Database)

	$ ./scripts/init.py

## Python Implementation

### Running the Parser (Python)

	$ docker-compose up

### Stopping the Parser (Python)

	$ docker-compose down

## Java Implementation

### Compile (Java)

Please note: Docker is not (yet) used here.
Gradle and java build tools have to be installed.

	$ ./scripts/compile_java.py

### Running the Parser (Java)

	$ docker-compose -f docker-compose.java.yaml up

### Stopping the Parser (Java)

	$ docker-compose -f docker-compose.java.yaml down

## Cleaning the Database

	$ docker-compose down
	$ rm -r runtime_data
