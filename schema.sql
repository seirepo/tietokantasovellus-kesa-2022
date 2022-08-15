CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    role INTEGER
);

CREATE TABLE IF NOT EXISTS sets (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users ON DELETE CASCADE,
    name TEXT,
    description TEXT,
    term TEXT DEFAULT 'term',
    definition TEXT DEFAULT 'definition',
    private INT,
    creation_time TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cards (
    id SERIAL PRIMARY KEY,
    set_id INTEGER REFERENCES sets ON DELETE CASCADE,
    word1 TEXT,
    word2 TEXT
);

CREATE TABLE IF NOT EXISTS latest_games (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    set_id INTEGER REFERENCES sets ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS card_results (
    id SERIAL PRIMARY KEY,
    latest_game_id INTEGER REFERENCES latest_games ON DELETE CASCADE,
    card_id INTEGER REFERENCES cards ON DELETE CASCADE,
    correctly_guessed INT,
    times_played INT
);
