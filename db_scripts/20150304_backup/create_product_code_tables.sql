drop table scin_db.pub_product_info;
create table scin_db.pub_product_info
(
  supplier      VARCHAR(100),
  catalog_nb    VARCHAR(100),
  product_desc  VARCHAR(200),
  url           VARCHAR(200),
  application   VARCHAR(300),
  host          VARCHAR(100),
  immunogen     VARCHAR(1500),
  reactivity_human    INT(1),         -- split into human / mouse
  reactivity_mouse    INT(1),
  CONSTRAINT    pk_product_info PRIMARY KEY (supplier, catalog_nb)
);

drop table scin_db.pub_product_name;
create table scin_db.pub_product_name
(
  supplier      VARCHAR(100),
  catalog_nb    VARCHAR(100),
  name1         VARCHAR(40),
  name2         VARCHAR(40),
  name3         VARCHAR(40),
  name4         VARCHAR(40),
  name5         VARCHAR(40),
  FOREIGN KEY (supplier, catalog_nb) REFERENCES scin_db.pub_product_info(supplier, catalog_nb)
);

