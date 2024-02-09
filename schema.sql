DROP TABLE IF EXISTS books;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    balance INTEGER NOT NULL
);

-- {
--  "id": integer, # A numeric ID
--  "title": "string", # A book title string
--  "author": "string", # A book author string
--  "genre": "string", # A genre string
--  "price": float # A real number price
-- }