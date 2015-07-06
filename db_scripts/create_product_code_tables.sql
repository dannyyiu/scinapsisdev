-- add a new column id
drop table scin_db.pub_product_info;
create table scin_db.pub_product_info
(
  id            INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  supplier_id   INT(11),
  supplier      VARCHAR(100),
  catalog_nb    VARCHAR(100),
  product_desc  VARCHAR(200),
  url           VARCHAR(200),
  application   VARCHAR(300),
  host          VARCHAR(100),
  immunogen     VARCHAR(1500),
  reactivity_human    INT(1),         -- split into human / mouse
  reactivity_mouse    INT(1),
  size          VARCHAR(10),
  price_usd     NUMERIC(10,2),
  primary_accession   VARCHAR(20),
  otheraccession      VARCHAR(300),
  gen_name            VARCHAR(20),
  antigen_region      VARCHAR(20),
  antigen_source      VARCHAR(150),
  clonality           VARCHAR(10),
  FOREIGN KEY (supplier_id) REFERENCES scin_db.pub_supplier_list(id)
);

-- consolidate [supplier_name, catalog_nb] into [prod_id]
drop table scin_db.pub_product_name;
create table scin_db.pub_product_name
(
  id            INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  prod_id       INT(11),
  name1         VARCHAR(40),
  name2         VARCHAR(40),
  name3         VARCHAR(40),
  name4         VARCHAR(40),
  name5         VARCHAR(40),
  name_summary  VARCHAR(200)
  FOREIGN KEY (prod_id) REFERENCES scin_db.pub_product_info(id)
);
