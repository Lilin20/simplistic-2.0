-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Erstellungszeit: 03. Jun 2022 um 07:46
-- Server-Version: 10.3.34-MariaDB-0+deb10u1
-- PHP-Version: 7.4.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `simplistic`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `case_items`
--

CREATE TABLE `case_items` (
  `item_id` int(11) NOT NULL,
  `item_name` varchar(255) DEFAULT NULL,
  `item_description` varchar(255) DEFAULT NULL,
  `item_price` int(11) DEFAULT NULL,
  `item_type` varchar(255) DEFAULT NULL,
  `item_rarity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `economy`
--

CREATE TABLE `economy` (
  `id` int(11) NOT NULL,
  `d_id` varchar(100) DEFAULT NULL,
  `money` int(11) DEFAULT NULL,
  `robbed_success` int(11) DEFAULT 0,
  `robbed_fail` int(11) DEFAULT 0,
  `worked_hours` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `userdata`
--

CREATE TABLE `userdata` (
  `d_id` varchar(100) NOT NULL,
  `lvl` int(11) DEFAULT NULL,
  `warns` int(11) DEFAULT NULL,
  `msg` int(11) DEFAULT NULL,
  `join_date` varchar(100) DEFAULT NULL,
  `xp` int(11) DEFAULT NULL,
  `growth` float DEFAULT NULL,
  `description` varchar(100) DEFAULT 'Nothing'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Daten für Tabelle `userdata`
--

INSERT INTO `userdata` (`d_id`, `lvl`, `warns`, `msg`, `join_date`, `xp`, `growth`, `description`) VALUES
('123321', 1337, 0, 12, 'Gestern', 1111, 0.25, 'Nothing');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `warns`
--

CREATE TABLE `warns` (
  `warn_id` int(11) NOT NULL,
  `warn_info` text DEFAULT NULL,
  `user_id` varchar(100) DEFAULT NULL,
  `warn_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `case_items`
--
ALTER TABLE `case_items`
  ADD PRIMARY KEY (`item_id`);

--
-- Indizes für die Tabelle `economy`
--
ALTER TABLE `economy`
  ADD PRIMARY KEY (`id`),
  ADD KEY `d_id` (`d_id`);

--
-- Indizes für die Tabelle `userdata`
--
ALTER TABLE `userdata`
  ADD PRIMARY KEY (`d_id`);

--
-- Indizes für die Tabelle `warns`
--
ALTER TABLE `warns`
  ADD PRIMARY KEY (`warn_id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `case_items`
--
ALTER TABLE `case_items`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `economy`
--
ALTER TABLE `economy`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `warns`
--
ALTER TABLE `warns`
  MODIFY `warn_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `economy`
--
ALTER TABLE `economy`
  ADD CONSTRAINT `d_id` FOREIGN KEY (`d_id`) REFERENCES `userdata` (`d_id`);

--
-- Constraints der Tabelle `warns`
--
ALTER TABLE `warns`
  ADD CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `userdata` (`d_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
