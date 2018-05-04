CREATE TABLE `proxy_ip` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ip` varchar(16) NOT NULL,
  `port` int(7) unsigned NOT NULL,
  `server_address` varchar(60) DEFAULT NULL,
  `anonymous` varchar(10) DEFAULT NULL,
  `type` varchar(8) NOT NULL COMMENT '类型',
  `speed` float(8,4) NOT NULL,
  `con_time` float(8,4) NOT NULL,
  `alive_time` varchar(10) NOT NULL COMMENT '存活时间',
  `check_time` varchar(16) NOT NULL COMMENT '验证时间',
  `status` tinyint(2) unsigned NOT NULL DEFAULT '1' COMMENT '0 => 不可用, 1=>可用',
  `created_at` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `updated_at` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '修改时间',
  PRIMARY KEY (`id`),
  KEY `speed` (`speed`),
  KEY `con_time` (`con_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;