

CREATE TABLE IF NOT EXISTS keywords (
	keyword TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL, 
  age INTEGER,
  gender TEXT,
  nationality TEXT
);

CREATE TABLE IF NOT EXISTS tweets (
  id INT PRIMARY KEY,
  name TEXT NOT NULL, 
  age INTEGER,
  gender TEXT,
  nationality TEXT,
	user_id INT,
	FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS keywords_tweets_rel (
	keyword TEXT,
  tweet_id INT,
	FOREIGN KEY (keyword) REFERENCES keywords(keyword),
	FOREIGN KEY (tweet_id) REFERENCES tweets(id)
);

INSERT INTO keywords (keyword) VALUES( 'adidas' );
INSERT INTO keywords (keyword) VALUES( 'puma' );
INSERT INTO keywords (keyword) VALUES( 'nike' );
