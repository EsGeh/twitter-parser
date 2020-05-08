#!/usr/bin/env python3


import psycopg2
from os import environ


def init_db():
    connection = psycopg2.connect(
        host = "twitter_parser_db",
        user = "postgres",
        database = "db",
    )
    connection.autocommit = True

    '''
    cursor = connection.cursor()

    # exec sql statement
    cursor.execute(
        # sql stmt:
        """...
        """
    )
    connection.commit()
    '''

    return connection


if __name__ == '__main__':
    print( "connecting to database..." )
    init_db()
