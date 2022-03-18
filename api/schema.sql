DROP TABLE IF EXISTS special;
DROP TABLE IF EXISTS general;

CREATE TABLE special (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    day TEXT,
    name TEXT,
    location TEXT,
    station TEXT,
    category TEXT
);

CREATE TABLE general (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    location TEXT,
    category TEXT
);