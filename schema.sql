DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    balance INTEGER NOT NULL
);
DROP TABLE IF EXISTS wallet;

<<<<<<< HEAD
CREATE TABLE wallet (
    wallet_id INTEGER PRIMARY KEY,
    balance INTEGER NOT NULL,
    wallet_user_id INTEGER,
    wallet_user_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (wallet_user_id) REFERENCES users(user_id)
);









DROP TABLE IF EXISTS station;
CREATE TABLE station (
    station_id INTEGER PRIMARY KEY AUTOINCREMENT,
    station_name TEXT NOT NULL,
    longitude FLOAT NOT NULL,
    latitude FLOAT NOT NULL
);

DROP TABLE IF EXISTS train;
CREATE TABLE train(
    train_id INTEGER PRIMARY KEY AUTOINCREMENT,
    train_name TEXT NOT NULL,
    capacity INTEGER NOT NULL,
    service_start TEXT NOT NULL,
    service_ends TEXT NOT NULL
);

DROP TABLE IF EXISTS train_stop;
CREATE TABLE train_stop(
    stop_id INTEGER PRIMARY KEY AUTOINCREMENT,
    train_id INTEGER NOT NULL,
    station_id INTEGER NOT NULL,
    arrival_time TEXT, 
    departure_time TEXT ,
    fare INTEGER NOT NULL,
    FOREIGN KEY (train_id) REFERENCES train(train_id) ON DELETE SET NULL,
    FOREIGN KEY (station_id) REFERENCES station(station_id) ON DELETE SET NULL
);
=======
>>>>>>> 96b01005a5d228e9fef1aa1c1edf044062ac1d86
-- {
--  "id": integer, # A numeric ID
--  "title": "string", # A book title string
--  "author": "string", # A book author string
--  "genre": "string", # A genre string
--  "price": float # A real number price
-- }
