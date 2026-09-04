CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    email TEXT NOT NULL,
    display_name TEXT NOT NULL,
    legacy_flag BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);
