#!/usr/bin/env python3


import psycopg2


#########################
# database abstraction:
#########################

def init():
    connection = psycopg2.connect(
        host = "twitter_parser_db",
        user = "postgres",
        database = "db",
    )
    connection.autocommit = True
    return connection

def get_keywords(connection):
    cursor = connection.cursor()
    cursor.execute(
        """SELECT (keyword) FROM keywords;"""
    )
    ret = cursor.fetchall()
    return list(map( lambda x: x[0], ret))

def write_tweet(
        db_connection,
        keyword,
        tweet_json,
):
    cursor = db_connection.cursor()
    # test if tweet already in db:
    cursor.execute(
        """
        SELECT (id)
        FROM tweets
        WHERE id=%(id)s;
        """,
        {
            "id": tweet_json['id_str'],
        }
    )
    ret = cursor.fetchall()
    # if already in database, do nothing:
    if( len(ret) > 0 ):
        print( f"already in db: '{tweet_json['id']}'" )
        return
    else:
        # add user:
        cursor.execute(
            """
            SELECT (id)
            FROM users
            WHERE id=%(user_id)s;
            """,
            {
                "user_id": tweet_json['user']['id_str'],
            }
        )
        ret = cursor.fetchall()
        if len(ret) == 0:
            cursor.execute(
                """
                INSERT INTO users (id,name)
                VALUES (%(user_id)s, %(user_name)s);
                """,
                {
                    "user_id": tweet_json['user']['id_str'],
                    "user_name": tweet_json['user']['name'],
                }
            )
        cursor.execute(
            """
            INSERT INTO tweets (id,text,user_id)
            VALUES (%(id)s, %(text)s, %(user_id)s);
            """,
            {
                "id": tweet_json['id_str'],
                "text": tweet_json['text'],
                "user_id": tweet_json['user']['id_str'],
            }
        )
        db_connection.commit()
    # remember (keyword, tweet):
    cursor.execute(
        """
        SELECT (keyword)
        FROM keywords_tweets_rel
        WHERE keyword=%(keyword)s AND tweet_id=%(tweet_id)s;
        """,
        {
            "keyword": keyword,
            "tweet_id": tweet_json['id_str'],
        }
    )
    ret = cursor.fetchall()
    # if already in database, do nothing:
    if( len(ret) > 0 ):
        print( f"already in db: '{tweet_json['id']}'" )
        return
    else:
        cursor.execute(
            """
            INSERT INTO keywords_tweets_rel
            VALUES (%(keyword)s, %(tweet_id)s);
            """,
            {
                "keyword": keyword,
                "tweet_id": tweet_json['id_str'],
            }
        )
        db_connection.commit()
