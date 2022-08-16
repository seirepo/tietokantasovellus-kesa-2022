CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS sets (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    term TEXT DEFAULT 'term',
    definition TEXT DEFAULT 'definition',
    private INT DEFAULT 0,
    creation_time TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS cards (
    id SERIAL PRIMARY KEY,
    set_id INTEGER REFERENCES sets ON DELETE CASCADE,
    word1 TEXT NOT NULL,
    word2 TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS latest_games (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    set_id INTEGER REFERENCES sets ON DELETE CASCADE,
    answer_with TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS card_results (
    latest_game_id INTEGER REFERENCES latest_games ON DELETE CASCADE,
    card_id INTEGER REFERENCES cards ON DELETE CASCADE,
    result INT DEFAULT 0,
    times_guessed_wrong INT DEFAULT 0
);
