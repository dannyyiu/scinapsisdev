DROP TABLE scin_db.pub_supplier_list;
CREATE TABLE scin_db.pub_supplier_list (
  supplier_name       VARCHAR(100)
);

INSERT INTO scin_db.pub_supplier_list (supplier_name) values ('Novus');
COMMIT;
