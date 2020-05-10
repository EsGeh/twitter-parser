

CREATE TABLE IF NOT EXISTS keywords (
	keyword TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tweets (
  id TEXT PRIMARY KEY,
	text TEXT,
	user_id TEXT NOT NULL,
	FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS keywords_tweets_rel (
	keyword TEXT NOT NULL,
  tweet_id TEXT NOT NULL,
	FOREIGN KEY (keyword) REFERENCES keywords(keyword),
	FOREIGN KEY (tweet_id) REFERENCES tweets(id)
);

INSERT INTO keywords (keyword) VALUES( 'adidas' );
INSERT INTO keywords (keyword) VALUES( 'puma' );
INSERT INTO keywords (keyword) VALUES( 'nike' );
