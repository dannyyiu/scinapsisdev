DROP TABLE scin_db.figure_tech;
CREATE TABLE scin_db.figure_tech (
  id                    INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  figure_id             INT(11),
  tech_id               INT(11),
  technique_group       VARCHAR(100),
  tech_parental_name    VARCHAR(100),
  tech_alternative      VARCHAR(100),
  doc_id                INT(11), 
  header                VARCHAR(800), 
  content               LONGTEXT,
  CONSTRAINT fk_fig_tech_figure_id FOREIGN KEY (figure_id) REFERENCES scin_db.scin_pub_figure(id),
  CONSTRAINT fk_fig_tech_tech_id FOREIGN KEY (tech_id) REFERENCES scin_db.pub_technique_list(id)
);