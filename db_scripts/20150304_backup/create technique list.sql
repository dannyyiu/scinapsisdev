DROP TABLE scin_db.pub_technique_list;
CREATE TABLE scin_db.pub_technique_list
(
  parental_name    VARCHAR(100),
  alternative     VARCHAR(100)
);

INSERT INTO scin_db.pub_technique_list VALUES ('Immunofluorescence','Immunofluorescence');
INSERT INTO scin_db.pub_technique_list VALUES ('Immunofluorescence','immunostaining');
INSERT INTO scin_db.pub_technique_list VALUES ('Immunofluorescence','confocal microscopy');
INSERT INTO scin_db.pub_technique_list VALUES ('Immunofluorescence','staining');
INSERT INTO scin_db.pub_technique_list VALUES ('Immunofluorescence','fluorescence microscopy');
INSERT INTO scin_db.pub_technique_list VALUES ('Immunofluorescence','microscopy');
INSERT INTO scin_db.pub_technique_list VALUES ('Immunofluorescence','IF');

INSERT INTO scin_db.pub_technique_list VALUES ('Immunoprecipitation','Immunoprecipitation');
INSERT INTO scin_db.pub_technique_list VALUES ('Immunoprecipitation','IP');
INSERT INTO scin_db.pub_technique_list VALUES ('Immunoprecipitation','Co-immunoprecipitation');
INSERT INTO scin_db.pub_technique_list VALUES ('Immunoprecipitation','Co-IP');
INSERT INTO scin_db.pub_technique_list VALUES ('Immunoprecipitation','Co-precipitate(s)(ed)');
INSERT INTO scin_db.pub_technique_list VALUES ('Immunoprecipitation','precipitate(s)(ed)');

INSERT INTO scin_db.pub_technique_list VALUES ('Western blot','Western blot');
INSERT INTO scin_db.pub_technique_list VALUES ('Western blot','immunoblotting');
INSERT INTO scin_db.pub_technique_list VALUES ('Western blot','SDS-PAGE');
INSERT INTO scin_db.pub_technique_list VALUES ('Western blot','Western blotting');

INSERT INTO scin_db.pub_technique_list VALUES ('Chromatin Immunoprecipitation','Chromatin Immunoprecipitation');
INSERT INTO scin_db.pub_technique_list VALUES ('Chromatin Immunoprecipitation','ChIP');

INSERT INTO scin_db.pub_technique_list VALUES ('Immunohistochemistry','Immunohistochemistry');
INSERT INTO scin_db.pub_technique_list VALUES ('Immunohistochemistry','IHC');
INSERT INTO scin_db.pub_technique_list VALUES ('ELISA','ELISA');

INSERT INTO scin_db.pub_technique_list VALUES ('FACS','FACS');
INSERT INTO scin_db.pub_technique_list VALUES ('FACS','flow cytometry');
