DROP TABLE scin_db.pub_supplier_list;
CREATE TABLE scin_db.pub_supplier_list (
  id             INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
  supplier       VARCHAR(100)
);

INSERT INTO scin_db.pub_supplier_list (supplier) values ('Novus');
INSERT INTO scin_db.pub_supplier_list (supplier) values ('Abgent');
COMMIT;


