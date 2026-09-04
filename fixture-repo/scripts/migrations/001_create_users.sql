-- Applied 2023-01-01
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    email TEXT NOT NULL,
    display_name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);
