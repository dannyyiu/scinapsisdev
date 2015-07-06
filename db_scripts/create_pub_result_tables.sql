-- consolidate [tech_parental_name, tech_alternative] into [tech_id]
DROP TABLE scin_db.pub_technique_result;
CREATE TABLE scin_db.pub_technique_result (
  id                    INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  doc_id                INT(11),
  tech_id               INT(11),
  technique_group       VARCHAR(100),
  tech_parental_name    VARCHAR(100),
  tech_alternative      VARCHAR(100),
  CONSTRAINT fk_tech_rslt_doc_id FOREIGN KEY (doc_id) REFERENCES scin_db.scin_pub_meta(id),
  CONSTRAINT fk_tech_rslt_tech_id FOREIGN KEY (tech_id) REFERENCES scin_db.pub_technique_list(id)
);

DROP TABLE scin_db.pub_supplier_result;
CREATE TABLE scin_db.pub_supplier_result (
  id                    INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  doc_id                INT(11),
  supplier_id           INT(11),
  supplier              VARCHAR(100),
  FOREIGN KEY (doc_id) REFERENCES scin_db.scin_pub_meta(id)
);

-- rename pub_prod_result to pub_product_result
-- consolidate [supplier_name, catalog_nb] into [prod_id]
DROP TABLE scin_db.pub_product_result;
CREATE TABLE scin_db.pub_product_result (
  id                    INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  doc_id                INT(11),
  prod_id               INT(11),
  supplier              VARCHAR(100),
  catalog_nb            VARCHAR(100),
  CONSTRAINT fk_product_rslt_doc_id FOREIGN KEY (doc_id) REFERENCES scin_db.scin_pub_meta(id),
  CONSTRAINT fk_product_rslt_prod_id FOREIGN KEY (prod_id) REFERENCES scin_db.pub_product_info(id)
);

-- temporary table to keep temp search result for regex process
-- doc_id points to scin_pub_meta; figure_id points to scin_pub_figure
DROP TABLE scin_db.pub_tech_prod_temp;
CREATE TABLE scin_db.pub_tech_prod_temp (
  doc_id                INT(11),
  figure_id             INT(11),
  si_id                 INT(11),
  tech_id               INT(11),
  technique_group       VARCHAR(100),
  tech_parental_name    VARCHAR(100),
  tech_alternative      VARCHAR(100),
  supplier              VARCHAR(100),
  prod_id               INT(11),
  catalog_nb            VARCHAR(100),
  prod_name_id          INT(11),
  product_name          VARCHAR(40),
  content               LONGTEXT,
  CONSTRAINT fk_tech_prod_temp_doc_id FOREIGN KEY (doc_id) REFERENCES scin_db.scin_pub_meta(id),
  CONSTRAINT fk_tech_prod_temp_fig_id FOREIGN KEY (figure_id) REFERENCES scin_db.scin_pub_figure(id),
  CONSTRAINT fk_tech_prod_temp_tech_id FOREIGN KEY (tech_id) REFERENCES scin_db.pub_technique_list(id),
  CONSTRAINT fk_tech_prod_temp_prod_id FOREIGN KEY (prod_id) REFERENCES scin_db.pub_product_info(id),
  CONSTRAINT fk_tech_prod_temp_prod_name_id FOREIGN KEY (prod_name_id) REFERENCES scin_db.pub_product_name(id)
);

DROP TABLE scin_db.pub_tech_prod_result;
CREATE TABLE scin_db.pub_tech_prod_result (
  id                    INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  doc_id                INT(11),
  figure_id             INT(11),
  si_id                 INT(11),
  tech_id               INT(11),
  technique_group       VARCHAR(100),
  tech_parental_name    VARCHAR(100),
  tech_alternative      VARCHAR(100),
  prod_id               INT(11),
  supplier              VARCHAR(100),
  catalog_nb            VARCHAR(100),
  prod_name_id          INT(11),
  product_name          VARCHAR(40),
  sentence              LONGTEXT,
  rating                INT(3),
  CONSTRAINT fk_tech_prod_rslt_doc_id FOREIGN KEY (doc_id) REFERENCES scin_db.scin_pub_meta(id),
  CONSTRAINT fk_tech_prod_rslt_fig_id FOREIGN KEY (figure_id) REFERENCES scin_db.scin_pub_figure(id),
  CONSTRAINT fk_tech_prod_rslt_tech_id FOREIGN KEY (tech_id) REFERENCES scin_db.pub_technique_list(id),
  CONSTRAINT fk_tech_prod_rslt_prod_id FOREIGN KEY (prod_id) REFERENCES scin_db.pub_product_info(id),
  CONSTRAINT fk_tech_prod_rslt_prod_name_id FOREIGN KEY (prod_name_id) REFERENCES scin_db.pub_product_name(id)
);
