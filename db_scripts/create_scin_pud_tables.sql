CREATE TABLE `scin_pub_meta` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `doc_id` varchar(100) DEFAULT NULL,
  `src_address` varchar(200),
  `pdf_address` varchar(200),
  `publisher` varchar(100) NOT NULL,
  `title` varchar(800) NOT NULL,
  `editors` varchar(200) NOT NULL,
  `pub_date` date NOT NULL,
  `copyright` longtext NOT NULL,
  `data_availibility` longtext NOT NULL,
  `funding` longtext NOT NULL,
  `competing_interest` longtext NOT NULL,
  `rec_update_time` datetime NOT NULL,
  `rec_update_by` varchar(20) NOT NULL,
  `citation` varchar(800),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=64846 DEFAULT CHARSET=utf8;

CREATE TABLE `scin_pub_material_n_method` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `section_id` int(11) NOT NULL,
  `header` varchar(800) NOT NULL,
  `content_seq` int(11) NOT NULL,
  `content` longtext NOT NULL,
  `doc_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `scin_pub_material_n_method_a80f21cf` (`doc_id`),
  CONSTRAINT `scin_pub_material_n_metho_doc_id_4f700606_fk_scin_pub_meta_id` FOREIGN KEY (`doc_id`) REFERENCES `scin_pub_meta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `scin_pub_figure` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `figure_id` int(11) NOT NULL,
  `header` varchar(800) NOT NULL,
  `content` longtext NOT NULL,
  `url` varchar(100) NOT NULL,
  `doc_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `scin_pub_figure_a80f21cf` (`doc_id`),
  CONSTRAINT `scin_pub_figure_doc_id_1d7d0f61_fk_scin_pub_meta_id` FOREIGN KEY (`doc_id`) REFERENCES `scin_pub_meta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `scin_pub_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `section_id` int(11) NOT NULL,
  `header` varchar(800) NOT NULL,
  `content_seq` int(11) NOT NULL,
  `content` longtext NOT NULL,
  `doc_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `scin_pub_result_a80f21cf` (`doc_id`),
  CONSTRAINT `scin_pub_result_doc_id_331d80e0_fk_scin_pub_meta_id` FOREIGN KEY (`doc_id`) REFERENCES `scin_pub_meta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `scin_pub_support_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `section_id` int(11) NOT NULL,
  `header` varchar(800) NOT NULL,
  `content` longtext NOT NULL,
  `url` varchar(100) NOT NULL,
  `doc_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `scin_pub_support_info_a80f21cf` (`doc_id`),
  CONSTRAINT `scin_pub_support_info_doc_id_5e0731a5_fk_scin_pub_meta_id` FOREIGN KEY (`doc_id`) REFERENCES `scin_pub_meta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
