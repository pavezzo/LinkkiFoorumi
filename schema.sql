CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT,
    admin BOOLEAN
);

CREATE TABLE links (
    link_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users,
    url TEXT,
    title TEXT,
    created_at TIMESTAMP
);

CREATE TABLE text_posts (
    post_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users,
    title TEXT,
    post_content TEXT,
    created_at TIMESTAMP
);