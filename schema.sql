DROP TABLE IF EXISTS users;
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    balance INTEGER NOT NULL
);

-- DROP TABLE IF EXISTS tickets
-- CREATE TABLE tickets (
--     ticket_id INTEGER PRIMARY KEY,
--     wallet_id INTEGER
--
--
--     FOREIGN KEY (wallet_id) REFERENCES users(user_id)
-- );

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