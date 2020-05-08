

CREATE TABLE IF NOT EXISTS keywords (
	id SERIAL PRIMARY KEY,
	keyword TEXT
);

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL, 
  age INTEGER,
  gender TEXT,
  nationality TEXT
);

CREATE TABLE IF NOT EXISTS tweets (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL, 
  age INTEGER,
  gender TEXT,
  nationality TEXT,
	user_id INT FOREIGN KEY REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS keywords_tweets (
  keyword_id INT,
  tweet_id INT,
	FOREIGN KEY (keyword_id) REFERENCES keywords(id),
	FOREIGN KEY (tweet_id) REFERENCES tweets(id),
	UNIQUE (keyword_id, tweet_id)
);

INSERT INTO keywords (keyword) VALUES( 'adidas' );
INSERT INTO keywords (keyword) VALUES( 'puma' );
INSERT INTO keywords (keyword) VALUES( 'nike' );
