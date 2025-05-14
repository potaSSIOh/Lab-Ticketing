-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versione server:              10.4.28-MariaDB - mariadb.org binary distribution
-- S.O. server:                  Win64
-- HeidiSQL Versione:            12.5.0.6677
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dump della struttura del database labticketing
CREATE DATABASE IF NOT EXISTS `labticketing` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;
USE `labticketing`;

-- Dump della struttura di tabella labticketing.aule
CREATE TABLE IF NOT EXISTS `aule` (
  `nAula` int(3) NOT NULL,
  `Lab` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`nAula`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dump dei dati della tabella labticketing.aule: ~3 rows (circa)
REPLACE INTO `aule` (`nAula`, `Lab`) VALUES
	(147, 1),
	(247, 1),
	(347, 1);

-- Dump della struttura di tabella labticketing.box
CREATE TABLE IF NOT EXISTS `box` (
  `codBox` varchar(30) NOT NULL,
  PRIMARY KEY (`codBox`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dump dei dati della tabella labticketing.box: ~2 rows (circa)
REPLACE INTO `box` (`codBox`) VALUES
	('1'),
	('2');

-- Dump della struttura di tabella labticketing.fissi
CREATE TABLE IF NOT EXISTS `fissi` (
  `HostName` varchar(40) NOT NULL,
  `Aula` int(3) NOT NULL,
  PRIMARY KEY (`HostName`),
  KEY `Aula` (`Aula`),
  CONSTRAINT `fissi_ibfk_1` FOREIGN KEY (`Aula`) REFERENCES `aule` (`nAula`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dump dei dati della tabella labticketing.fissi: ~4 rows (circa)
REPLACE INTO `fissi` (`HostName`, `Aula`) VALUES
	('W10STAT-7-146', 247),
	('W10STAT-7-162', 247),
	('W10STAT-7-163', 247),
	('W10STAT-7-234', 347);

-- Dump della struttura di tabella labticketing.portatili
CREATE TABLE IF NOT EXISTS `portatili` (
  `hostname` varchar(40) NOT NULL,
  `codBox` varchar(30) NOT NULL,
  PRIMARY KEY (`hostname`),
  KEY `codBox` (`codBox`),
  CONSTRAINT `portatili_ibfk_1` FOREIGN KEY (`codBox`) REFERENCES `box` (`codBox`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dump dei dati della tabella labticketing.portatili: ~2 rows (circa)
REPLACE INTO `portatili` (`hostname`, `codBox`) VALUES
	('233', '1'),
	('332', '2');

-- Dump della struttura di tabella labticketing.ticketf
CREATE TABLE IF NOT EXISTS `ticketf` (
  `IdTicket` int(11) NOT NULL AUTO_INCREMENT,
  `descrizione` varchar(50) NOT NULL,
  `dataOra` datetime NOT NULL DEFAULT current_timestamp(),
  `creatore` int(4) NOT NULL,
  `hostnameF` varchar(40) DEFAULT NULL,
  `tecnico` int(11) DEFAULT NULL,
  `stato` varchar(14) DEFAULT NULL,
  PRIMARY KEY (`IdTicket`),
  KEY `creatore` (`creatore`),
  KEY `hostnameF` (`hostnameF`),
  KEY `tecnico` (`tecnico`),
  CONSTRAINT `ticketf_ibfk_1` FOREIGN KEY (`creatore`) REFERENCES `utenti` (`id`),
  CONSTRAINT `ticketf_ibfk_2` FOREIGN KEY (`hostnameF`) REFERENCES `fissi` (`HostName`),
  CONSTRAINT `ticketf_ibfk_4` FOREIGN KEY (`tecnico`) REFERENCES `utenti` (`id`),
  CONSTRAINT `check_stato` CHECK (`stato` in ('In lavorazione','Chiuso','Aperto'))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dump dei dati della tabella labticketing.ticketf: ~1 rows (circa)
REPLACE INTO `ticketf` (`IdTicket`, `descrizione`, `dataOra`, `creatore`, `hostnameF`, `tecnico`, `stato`) VALUES
	(2, 'non funzion', '2025-05-14 12:37:12', 1, 'W10STAT-7-146', 1, 'Aperto');

-- Dump della struttura di tabella labticketing.ticketp
CREATE TABLE IF NOT EXISTS `ticketp` (
  `IdTicket` int(11) NOT NULL AUTO_INCREMENT,
  `descrizione` varchar(50) NOT NULL,
  `dataOra` datetime NOT NULL DEFAULT current_timestamp(),
  `creatore` int(4) NOT NULL,
  `hostnameP` varchar(40) DEFAULT NULL,
  `tecnico` int(11) DEFAULT NULL,
  `stato` varchar(14) DEFAULT NULL,
  PRIMARY KEY (`IdTicket`) USING BTREE,
  KEY `creatore` (`creatore`) USING BTREE,
  KEY `hostnameP` (`hostnameP`) USING BTREE,
  KEY `tecnico` (`tecnico`) USING BTREE,
  CONSTRAINT `ticketp_ibfk_1` FOREIGN KEY (`creatore`) REFERENCES `utenti` (`id`),
  CONSTRAINT `ticketp_ibfk_3` FOREIGN KEY (`hostnameP`) REFERENCES `portatili` (`hostname`),
  CONSTRAINT `ticketp_ibfk_4` FOREIGN KEY (`tecnico`) REFERENCES `utenti` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci ROW_FORMAT=DYNAMIC;

-- Dump dei dati della tabella labticketing.ticketp: ~1 rows (circa)
REPLACE INTO `ticketp` (`IdTicket`, `descrizione`, `dataOra`, `creatore`, `hostnameP`, `tecnico`, `stato`) VALUES
	(2, 'non funzion', '2025-05-14 12:36:42', 1, '233', 1, 'Aperto');

-- Dump della struttura di tabella labticketing.token
CREATE TABLE IF NOT EXISTS `token` (
  `token_number` varchar(64) NOT NULL,
  `user_id` int(11) NOT NULL,
  `expiration_date` datetime NOT NULL,
  PRIMARY KEY (`token_number`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `token_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `utenti` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dump dei dati della tabella labticketing.token: ~0 rows (circa)

-- Dump della struttura di tabella labticketing.utenti
CREATE TABLE IF NOT EXISTS `utenti` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `name_mail` varchar(50) NOT NULL,
  `password` varchar(20) NOT NULL,
  `autorizzato` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_mail` (`name_mail`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dump dei dati della tabella labticketing.utenti: ~1 rows (circa)
REPLACE INTO `utenti` (`id`, `name_mail`, `password`, `autorizzato`) VALUES
	(1, 'ilBoss', '123', 1);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
