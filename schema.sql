CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    role INTEGER
);

CREATE TABLE sets (
    id SERIAL PRIMARY KEY,
    name TEXT,
    creator_id INTEGER REFERENCES users,
    description TEXT,
    card_order INT,
    term TEXT DEFAULT 'term',
    definition TEXT DEFAULT 'definition',
    private INT
);

CREATE TABLE cards (
    id SERIAL PRIMARY KEY,
    set_id INTEGER REFERENCES sets,
    word1 TEXT,
    word2 TEXT
);
