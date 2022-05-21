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

CREATE TABLE comments (
    comment_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users,
    post_id INT REFERENCES text_posts,
    link_id INT REFERENCES links,
    comment TEXT,
    parent INT REFERENCES comments,
    created_at TIMESTAMP
);