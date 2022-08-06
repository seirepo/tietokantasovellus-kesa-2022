CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    role INTEGER
);

CREATE TABLE sets (
    id SERIAL PRIMARY KEY,
    creator_id INTEGER REFERENCES users,
    name TEXT,
    description TEXT,
    term TEXT DEFAULT 'term',
    definition TEXT DEFAULT 'definition',
    private INT
);

CREATE TABLE cards (
    id SERIAL PRIMARY KEY,
    set_id INTEGER REFERENCES sets ON DELETE CASCADE,
    word1 TEXT,
    word2 TEXT
);
