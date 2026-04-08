-- =============================================================
-- init.sql
-- Auto-executed on first PostgreSQL container startup.
-- Creates the users and calculations tables.
-- =============================================================

CREATE TABLE IF NOT EXISTS users (
    id         SERIAL PRIMARY KEY,
    username   VARCHAR(50)  NOT NULL UNIQUE,
    email      VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS calculations (
    id         SERIAL PRIMARY KEY,
    operation  VARCHAR(20)  NOT NULL,
    operand_a  FLOAT        NOT NULL,
    operand_b  FLOAT        NOT NULL,
    result     FLOAT        NOT NULL,
    timestamp  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    user_id    INTEGER      NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
