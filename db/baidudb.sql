CREATE DATABASE  IF NOT EXISTS `baidudb`;
USE `baidudb`;

--
-- Table structure for table `resitem`
--

DROP TABLE IF EXISTS `resitem`;
CREATE TABLE `resitem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9666 DEFAULT CHARSET=utf8;

--
-- Table structure for table `baiduitem`
--

DROP TABLE IF EXISTS `baiduitem`;
CREATE TABLE `baiduitem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  `url` longtext,
  `text` longtext,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Table structure for table `proxy`
--

DROP TABLE IF EXISTS `proxy`;
CREATE TABLE `proxy` (
  `id` varchar(45) NOT NULL,
  `ip` varchar(45) DEFAULT NULL,
  `port` varchar(45) DEFAULT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
