DROP TABLE scin_db.pub_technique_list;
CREATE TABLE scin_db.pub_technique_list
(
  id              INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  technique_group  VARCHAR(100),
  parental_name    VARCHAR(100),
  alternative     VARCHAR(100)
);

DELETE FROM scin_db.pub_technique_list;
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Immunostaining','Immunofluorescence','immunofluorescence');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Immunostaining','Immunofluorescence','immunostaining');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Immunostaining','Immunofluorescence','immunostained');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Immunostaining','Immunofluorescence','confocal microscopy');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Immunostaining','Immunofluorescence','stained');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Immunostaining','Immunofluorescence','staining');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Immunostaining','Immunofluorescence','fluorescence microscopy');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Immunostaining','Immunofluorescence','microscopy');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Immunostaining','Immunofluorescence','co-stained');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Immunostaining','Immunofluorescence','co-staining');

INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Immunoprecipitation','Immunoprecipitation','immunoprecipitation');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Immunoprecipitation','Immunoprecipitation','co-immunoprecipitation');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Immunoprecipitation','Immunoprecipitation','co-IP');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Immunoprecipitation','Immunoprecipitation','precipitates');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Immunoprecipitation','Immunoprecipitation','precipitated');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Immunoprecipitation','Immunoprecipitation','co-precipitates');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Immunoprecipitation','Immunoprecipitation','co-precipitated');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Immunoprecipitation','Immunoprecipitation','immunoprecipitates');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Immunoprecipitation','Immunoprecipitation','immunoprecipitated');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Immunoprecipitation','Immunoprecipitation','co-immunoprecipitates');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Immunoprecipitation','Immunoprecipitation','co-immunoprecipitated');


INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Western blot','Western blot','western blot');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Western blot','Western blot','immunoblot');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Western blot','Western blot','immunoblots');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Western blot','Western blot','immunoblotting');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Western blot','Western blot','immunoblotted');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Western blot','Western blot','SDS-PAGE');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Western blot','Western blot','SDS, PAGE');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Western blot','Western blot','western blotting');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Western blot','Western blot','western blots');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Western blot','Western blot','western blotted');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Western blot','Western blot','blotted');

INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Chromatin Immunoprecipitation','Chromatin Immunoprecipitation','Chromatin Immunoprecipitation');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Chromatin Immunoprecipitation','Chromatin Immunoprecipitation','ChIP');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Chromatin Immunoprecipitation','Chromatin Immunoprecipitation','ChIP-qPCR');

INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Immunostaining','Immunohistochemistry','Immunohistochemistry');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Immunostaining','Immunohistochemistry','IHC');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('Immunostaining','Immunohistochemistry','immunohistochemical');


INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('ELISA','ELISA','ELISA');

INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('FACS','FACS','FACS');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('FACS','FACS','flow cytometry');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('FACS','FACS','flow-cytometry');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('FACS','FACS','flow, cytometry');
INSERT INTO scin_db.pub_technique_list (technique_group, parental_name, alternative) VALUES ('FACS','FACS','flow cytometric');