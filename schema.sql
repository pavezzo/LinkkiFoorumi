DROP TABLE IF EXISTS users, links, text_posts, comments, subforums, subscriptions, likes; 

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    admin BOOLEAN
);

CREATE TABLE subforums (
    sub_id SERIAL PRIMARY KEY,
    owner_id INT REFERENCES users NOT NULL,
    sub_name VARCHAR(20) UNIQUE NOT NULL,
    introduction VARCHAR(300),
    created_at TIMESTAMP
);

CREATE TABLE links (
    link_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users NOT NULL,
    subforum_id INT REFERENCES subforums NOT NULL,
    url VARCHAR(1000) NOT NULL,
    title VARCHAR(30) NOT NULL,
    created_at TIMESTAMP
);

CREATE TABLE text_posts (
    post_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users NOT NULL,
    subforum_id INT REFERENCES subforums NOT NULL,
    title VARCHAR(30) NOT NULL,
    post_content VARCHAR(5000),
    created_at TIMESTAMP
);

CREATE TABLE comments (
    comment_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users NOT NULL,
    post_id INT REFERENCES text_posts ON DELETE CASCADE,
    link_id INT REFERENCES links ON DELETE CASCADE,
    comment VARCHAR(1000) NOT NULL,
    parent INT REFERENCES comments,
    created_at TIMESTAMP,
    visible BOOLEAN
);

CREATE TABLE subscriptions (
    subscription_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users NOT NULL,
    subforum_id INT REFERENCES subforums NOT NULL,
    created_at TIMESTAMP
);

CREATE TABLE likes (
    like_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users NOT NULL,
    link_id INT REFERENCES links ON DELETE CASCADE,
    post_id INT REFERENCES text_posts ON DELETE CASCADE,
    comment_id INT REFERENCES comments ON DELETE CASCADE,
    positive BOOLEAN NOT NULL
);