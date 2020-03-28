-- Users table
CREATE TABLE users (
    user_id serial PRIMARY KEY,
    user_name varchar(80),
    password varchar(100),
    email varchar(100),
    create_date timestamp DEFAULT CURRENT_TIMESTAMP,
    create_user varchar(80) DEFAULT CURRENT_USER
);

-- Status table
CREATE TABLE status (
    status_id serial PRIMARY KEY,
    status_code varchar(30),
    description text,
    create_date timestamp DEFAULT CURRENT_TIMESTAMP,
    create_user varchar(80) DEFAULT CURRENT_USER
);

-- Create Projects table
CREATE TABLE projects (
    project_id serial PRIMARY KEY,
    author_id integer REFERENCES users,
    assigned_id integer,
    status_id integer REFERENCES status,
    title varchar(200),
    description text,
    create_date timestamp DEFAULT CURRENT_TIMESTAMP
);

-- project comments table
CREATE TABLE project_comments (
    project_comment_id serial PRIMARY KEY,
    project_id integer REFERENCES projects ON DELETE CASCADE,
    author_id integer REFERENCES users,
    comment_text text,
    create_date timestamp DEFAULT CURRENT_TIMESTAMP
);

-- tasks table
CREATE TABLE tasks (
    task_id serial PRIMARY KEY,
    project_id integer REFERENCES projects ON DELETE CASCADE,
    author_id integer REFERENCES users,
    assigned_id integer,
    status_id integer REFERENCES status,
    title varchar(200),
    description text,
    create_date timestamp DEFAULT CURRENT_TIMESTAMP
);

-- task comments table
CREATE TABLE task_comments (
    task_comment_id serial PRIMARY KEY,
    task_id integer REFERENCES tasks ON DELETE CASCADE,
    author_id integer REFERENCES users,
    comment_text text,
    create_date timestamp DEFAULT CURRENT_TIMESTAMP
);

-- items table
CREATE TABLE items (
    item_id serial PRIMARY KEY,
    task_id integer REFERENCES tasks ON DELETE CASCADE,
    author_id integer REFERENCES users,
    status_id integer REFERENCES status,
    assigned_id integer,
    title varchar(200),
    description text,
    create_date timestamp DEFAULT CURRENT_TIMESTAMP
);

-- item comments table
CREATE TABLE item_comments (
    item_comment_id serial PRIMARY KEY,
    item_id integer REFERENCES items ON DELETE CASCADE,
    author_id integer REFERENCES users,
    comment_text text,
    create_date timestamp DEFAULT CURRENT_TIMESTAMP
);
