--
-- Table structure for table `blog`
--

DROP TABLE IF EXISTS `blog`;
CREATE TABLE `blog` (
  `id`      INT(11)     NOT NULL AUTO_INCREMENT,
  `title`   VARCHAR(40) NOT NULL,
  `content` TEXT        NOT NULL,
  `addDate` DATE        NOT NULL,
  `updDate` DATE        NOT NULL,
  `tag`     VARCHAR(40) NOT NULL DEFAULT '未分类',
  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

--
-- Table structure for table `list`
--

DROP TABLE IF EXISTS `list`;
CREATE TABLE `list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) NOT NULL,
  `state` tinyint(1) NOT NULL DEFAULT '0',
  `addDate` date NOT NULL,
  `comDate` date DEFAULT NULL,
  `score` int(11) NOT NULL,
  `isReview` tinyint(1) NOT NULL,
  `review` text,
  `tag` varchar(40) NOT NULL DEFAULT '未分类',
  PRIMARY KEY (`id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
