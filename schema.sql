CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT,
    admin BOOLEAN
);

CREATE TABLE links (
    link_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users,
    subforum_id INT REFERENCES subforums,
    url TEXT,
    title TEXT,
    created_at TIMESTAMP
);

CREATE TABLE text_posts (
    post_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users,
    subforum_id INT REFERENCES subforums,
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

CREATE TABLE subforums (
    sub_id SERIAL PRIMARY KEY,
    owner_id INT REFERENCES users,
    sub_name TEXT,
    introduction TEXT,
    created_at TIMESTAMP
);

CREATE TABLE subscriptions (
    subsricption_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users NOT NULL,
    subforum_id INT REFERENCES subforums NOT NULL,
    created_at TIMESTAMP
);