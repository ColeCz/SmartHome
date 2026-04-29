CREATE TABLE IF NOT EXISTS members (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    user_password VARCHAR NOT NULL,
    user_role VARCHAR DEFAULT 'standard'
);

