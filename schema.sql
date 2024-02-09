DROP TABLE IF EXISTS books;

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