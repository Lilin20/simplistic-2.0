CREATE DATABASE IF NOT EXISTS simplistic;
USE simplistic;

SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
    id            VARCHAR(255) NOT NULL PRIMARY KEY,
    username      VARCHAR(255) NOT NULL,
    level         INT NOT NULL,
    xp            INT NOT NULL,
    growth        FLOAT NOT NULL,
    messages      INT NOT NULL,
    warns         INT NOT NULL,
    status        VARCHAR(255) NOT NULL DEFAULT("No status set.")
);

DROP TABLE IF EXISTS economy;
CREATE TABLE IF NOT EXISTS economy (
    users_id      VARCHAR(255) NOT NULL,
    balance       INT NOT NULL,
    worked        INT NOT NULL,
    got_robbed    INT NOT NULL,
    has_robbed    INT NOT NULL,
    FOREIGN KEY(users_id) REFERENCES users(id) ON DELETE CASCADE
);

SET FOREIGN_KEY_CHECKS=0;