# CREATE TEMP TABLES
DROP TABLE scin_db.pub_technique_temp;
CREATE TABLE scin_db.pub_technique_temp (
    doc_id              INT(11) NOT NULL,
    tech_parental_name  VARCHAR(100) NOT NULL,
    tech_alternative    VARCHAR(100) NOT NULL,
    FOREIGN KEY (doc_id) REFERENCES scin_db.scin_pub_meta(id)
);

DROP TABLE scin_db.pub_protein_temp;
CREATE TABLE scin_db.pub_protein_temp (
    doc_id              INT(11) NOT NULL,
    protein_gene_name   VARCHAR(100) NOT NULL,
    FOREIGN KEY (doc_id) REFERENCES scin_pub_meta(id)
);

DROP TABLE scin_db.pub_tech_protein_temp;
CREATE TABLE scin_db.pub_tech_protein_temp (
    doc_id              INT(11) NOT NULL,
    protein_gene_name   VARCHAR(100) NOT NULL,
    tech_parental_name  VARCHAR(100) NOT NULL,
    tech_alternative    VARCHAR(100) NOT NULL,
    figure_id           INT(11) NOT NULL,
    content             LONGTEXT,
    FOREIGN KEY (doc_id) REFERENCES scin_pub_meta(id)
);

DROP TABLE scin_db.pub_tech_protein_result;
CREATE TABLE scin_db.pub_tech_protein_result (
    doc_id              INT(11) NOT NULL,
    protein_gene_name   VARCHAR(100) NOT NULL,
    tech_parental_name  VARCHAR(100) NOT NULL,
    tech_alternative    VARCHAR(100) NOT NULL,
    figure_id           INT(11) NOT NULL,
    sentence            LONGTEXT,
    FOREIGN KEY (doc_id) REFERENCES scin_pub_meta(id)
);