DROP DATABASE simplistic;
CREATE DATABASE IF NOT EXISTS simplistic;
USE simplistic;

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

CREATE TABLE IF NOT EXISTS economy (
    users_id      VARCHAR(255) NOT NULL,
    balance       INT NOT NULL,
    worked        INT NOT NULL,
    worked_hours  INT NOT NULL,
    got_robbed    INT NOT NULL,
    has_robbed    INT NOT NULL,
    rob_spree     INT NOT NULL,
    FOREIGN KEY(users_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS server_vars (
    name            VARCHAR(255) NOT NULL,
    value           INT NOT NULL
);

CREATE TABLE IF NOT EXISTS achievements (
    id              INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(255) NOT NULL,
    description     VARCHAR(255) NOT NULL,
    value           INT NOT NULL,
    type            VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS user_achievements (
    id              INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    users_id        VARCHAR(255) NOT NULL,
    achievements_id INT NOT NULL,
    FOREIGN KEY(users_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY(achievements_id) REFERENCES achievements(id) ON DELETE CASCADE
);

INSERT INTO server_vars (name, value) VALUES ("steuer", 5);
INSERT INTO server_vars (name, value) VALUES ("server_money", 0);
INSERT INTO server_vars (name, value) VALUES ("counting", 0);
INSERT INTO server_vars (name, value) VALUES ("counting_record", 0);





--Achievement Inserts...
INSERT INTO achievements (name, description, value, type) VALUES ("Moin Meister", "Erste Nachricht geschrieben.", 1, "message");
INSERT INTO achievements (name, description, value, type) VALUES ("In Gutenbergs Fußstapfen", "100 Nachrichten geschrieben", 100, "message");
INSERT INTO achievements (name, description, value, type) VALUES ("Teuflischer Dichter", "666 Nachrichten geschrieben", 666, "message");
INSERT INTO achievements (name, description, value, type) VALUES ("Message-Rambo", "1000 Nachrichten geschrieben.", 1000, "message");
INSERT INTO achievements (name, description, value, type) VALUES ("Crackhead", "2000 Nachrichten geschrieben", 2000, "message");

INSERT INTO achievements (name, description, value, type) VALUES ("Da hat sich das Amt gelohnt", "Erstes mal arbeiten gewesen.", 1, "economy_work");
INSERT INTO achievements (name, description, value, type) VALUES ("Arbeitstier", "10 mal arbeiten gewesen.", 10, "economy_work");
INSERT INTO achievements (name, description, value, type) VALUES ("Lohn verdient sich nicht von selbst", "25 mal arbeiten gewesen.", 25, "economy_work");
INSERT INTO achievements (name, description, value, type) VALUES ("Geld wächst nicht an Bäumen", "50 mal arbeiten gewesen.", 50, "economy_work");
INSERT INTO achievements (name, description, value, type) VALUES ("Mitarbeiter des Monats", "100 mal arbeiten gewesen.", 100, "economy_work");
INSERT INTO achievements (name, description, value, type) VALUES ("Mitarbeiter des Jahres", "250 mal arbeiten gewesen.", 250, "economy_work");
INSERT INTO achievements (name, description, value, type) VALUES ("CEO", "500 mal arbeiten gewesen.", 500, "economy_work");

INSERT INTO achievements (name, description, value, type) VALUES ("Geringverdiener", "Die ersten 100 verdient!", 100, "economy_money");
INSERT INTO achievements (name, description, value, type) VALUES ("Oh, 4 stellig", "Das erste mal 1.000 auf dem Konto.", 1000, "economy_money");
INSERT INTO achievements (name, description, value, type) VALUES ("Started from the bottom now i am here", "Das erste mal 5.000 auf dem Konto.", 5000, "economy_money");
INSERT INTO achievements (name, description, value, type) VALUES ("Oh, 5 stellig", "Das erste mal 10.000 auf dem Konto", 10000, "economy_money");
INSERT INTO achievements (name, description, value, type) VALUES ("Das sieht doch mal schmackhaft aus", "Das erste mal 50.000 auf dem Konto.", 50000, "economy_money");
INSERT INTO achievements (name, description, value, type) VALUES ("Oh, 6 stellig", "Das erste mal 100.000 auf dem Konto", 100000, "economy_money");
INSERT INTO achievements (name, description, value, type) VALUES ("Aus den Weg Geringverdiener!", "Das erste mal 500.000 auf dem Konto.", 500000, "economy_money");
INSERT INTO achievements (name, description, value, type) VALUES ("Wie schön es ist Millionär zu sein!", "Das erste mal 1.000.000 auf dem Konto.", 1000000, "economy_money");
INSERT INTO achievements (name, description, value, type) VALUES ("The Wold's Billionaires", "Das erste mal 1.000.000.000 auf dem Konto", 1000000000, "economy_money");

INSERT INTO achievements (name, description, value, type) VALUES ("Schmutziges Geld", "Das erste mal jemand erfolgreich ausgeraubt.", 1, "economy_rob_success");
INSERT INTO achievements (name, description, value, type) VALUES ("Zack, und weg", "10 mal jemand erfolgreich ausgeraubt.", 10, "economy_rob_success");
INSERT INTO achievements (name, description, value, type) VALUES ("Harlunke", "25 mal jemand erfolgreich ausgeraubt.", 25, "economy_rob_success");
INSERT INTO achievements (name, description, value, type) VALUES ("Find him, dead or alive...", "50 mal jemand erfolgreich ausgeraubt.", 50, "economy_rob_success");
INSERT INTO achievements (name, description, value, type) VALUES ("Auf der INTERPOL-Watchlist", "100 mal jemand erfolgreich ausgeraubt.", 100, "economy_rob_success");

INSERT INTO achievements (name, description, value, type) VALUES ("Totenstille und Fingerfertigkeit", "3 mal hintereinander jemanden erfolgreich ausgeraubt.", 3, "economy_rob_spree");
INSERT INTO achievements (name, description, value, type) VALUES ("System gedribbelt", "5 mal hintereinander jemanden erfolgreich ausgeraubt.", 5, "economy_rob_spree");

INSERT INTO achievements (name, description, value, type) VALUES ("Bug Finder", "Danke für das finden und melden eines Bugs!", 1, "manual");
INSERT INTO achievements (name, description, value, type) VALUES ("Gute Nudel Stern", "Einer der sehr cleanen User!", 1, "manual");
