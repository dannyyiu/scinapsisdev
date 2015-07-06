DROP TABLE scin_db.pub_technique_result;
CREATE TABLE scin_db.pub_technique_result (
  doc_id                INT(11),
  tech_parental_name    VARCHAR(100),
  tech_alternative      VARCHAR(100),
  FOREIGN KEY (doc_id) REFERENCES scin_db.scin_pub_meta(id)
);

DROP TABLE scin_db.pub_supplier_result;
CREATE TABLE scin_db.pub_supplier_result (
  doc_id                INT(11),
  supplier_name         VARCHAR(100),
  FOREIGN KEY (doc_id) REFERENCES scin_db.scin_pub_meta(id)
);

CREATE TABLE scin_db.pub_prod_result (
  doc_id                INT(11),
  supplier_name         VARCHAR(100),
  catalog_nb            VARCHAR(100),
  FOREIGN KEY (doc_id) REFERENCES scin_db.scin_pub_meta(id)
);

-- temporary table to keep temp search result for regex process
DROP TABLE scin_db.pub_tech_prod_temp;
CREATE TABLE scin_db.pub_tech_prod_temp (
  doc_id                INT(11),
  pub_figure_id         INT(11),
  tech_parental_name    VARCHAR(100),
  tech_alternative      VARCHAR(100),
  supplier_name         VARCHAR(100),
  catalog_nb            VARCHAR(100),
  product_name          VARCHAR(40),
  content               LONGTEXT,
  FOREIGN KEY (pub_figure_id) REFERENCES scin_db.scin_pub_meta(id)
);

DROP TABLE scin_db.pub_tech_prod_result;
CREATE TABLE scin_db.pub_tech_prod_result (
  doc_id                INT(11),
  pub_figure_id         INT(11),
  tech_parental_name    VARCHAR(100),
  tech_alternative      VARCHAR(100),
  supplier_name         VARCHAR(100),
  catalog_nb            VARCHAR(100),
  product_name          VARCHAR(40),
  sentence              LONGTEXT,
  FOREIGN KEY (pub_figure_id) REFERENCES scin_db.scin_pub_meta(id)
);
