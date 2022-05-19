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
);

CREATE TABLE contents (
    id SERIAL PRIMARY KEY,
    CONSTRAINT fk_link
        FOREIGN KEY(link_id)
            REFERENCES links(link_id),
    CONSTRAINT fk_post
        FOREIGN KEY(post_id)
            REFERENCES posts(post_id)
);