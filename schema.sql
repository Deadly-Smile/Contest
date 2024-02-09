DROP TABLE IF EXISTS books;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    balance INTEGER NOT NULL,
);

CREATE TABLE wallet (
    wallet_id INTEGER PRIMARY KEY,
    balance INTEGER NOT NULL,
    wallet_user_id INTEGER,
    wallet_user_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (wallet_user_id) REFERENCES users(user_id)
);

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT NOT NULL,
    price FLOAT NOT NULL
);

-- {
--  "id": integer, # A numeric ID
--  "title": "string", # A book title string
--  "author": "string", # A book author string
--  "genre": "string", # A genre string
--  "price": float # A real number price
-- }