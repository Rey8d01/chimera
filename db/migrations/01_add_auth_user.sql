-- +migrate Up
PRAGMA foreign_keys=ON;

CREATE TABLE auth_user
(
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    email      TEXT                           NOT NULL,
    pwd        TEXT                           NOT NULL,
    role       TEXT DEFAULT 'user'            NOT NULL,
    created_at TEXT DEFAULT (DATETIME('now')) NOT NULL
);

CREATE UNIQUE INDEX auth_user_email_uindex ON auth_user (email COLLATE NOCASE);

-- +migrate Down
DROP TABLE IF EXISTS auth_user;
