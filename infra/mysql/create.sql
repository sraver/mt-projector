
GRANT ALL PRIVILEGES ON app_db.* TO 'user'@'%' IDENTIFIED BY 'userpass';
GRANT SUPER ON *.* TO 'user'@'%' IDENTIFIED BY 'userpass';
FLUSH PRIVILEGES;

CREATE TABLE `raw_data` (
  `asset` varchar(15) NOT NULL,
  `timeframe` varchar(5) NOT NULL,
  `date` datetime NOT NULL,
  `open` double NOT NULL,
  `close` double NOT NULL,
  `high` double NOT NULL,
  `low` double NOT NULL,
  `volume` double NOT NULL,
  PRIMARY KEY (`asset`,`timeframe`,`date`),
  KEY `raw_data_asset_IDX` (`asset`,`timeframe`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
