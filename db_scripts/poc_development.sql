/*
* stored procedures caller
*/
-- validation script
truncate table scin_db.pub_protein_temp;
truncate table scin_db.pub_technique_temp;
truncate table scin_db.pub_tech_protein_temp;
-- truncate table scin_db.pub_tech_protein_result;
select * from scin_db.scin_pub_meta where id = 1;
select * from scin_db.scin_pub_material_n_method where doc_id_id = 2;
select * from scin_db.pub_technique_temp;
select * from scin_db.pub_protein_temp;
select * from scin_db.pub_tech_protein_temp;
select * from scin_db.pub_tech_protein_result where protein_gene_name <> 'A' and protein_gene_name <> 'T';
select count(distinct doc_id) from scin_db.pub_tech_protein_result where protein_gene_name <> 'A' and protein_gene_name <> 'T';

SELECT protein_gene_name, tech_parental_name, tech_alternative, figure_id, content FROM scin_db.pub_tech_protein_temp

SELECT * FROM scin_db.pub_tech_protein_result;
select count(1) from scin_db.pub_tech_protein_result;

select count(1) from scin_db.scin_pub_material_n_method;

-- SIMLATION: STEP 1a - search if protein exists
call scin_db.pub_technique_exists(1);
select * from scin_db.pub_technique_result;

-- SIMLATION: STEP 1b - search if protein exists
call scin_db.pub_supplier_exists(17590);
select * from scin_db.pub_supplier_result;

truncate table scin_db.pub_technique_result;
truncate table scin_db.pub_supplier_result;

-- STEP 2 - search if protein and technique exists in same sentence
call scin_db.pub_technique_protein_exists(4);
select * from scin_db.pub_tech_protein_temp;




SELECT 1
  FROM scin_db.scin_pub_figure
  WHERE doc_id_id = 2
  AND figure_id = 4
  AND (CONTENT LIKE '%UBD%')


-- SIMLATION: STEP 3 - search if protein exists
call scin_db.pub_protein_exists(1);
select * from scin_db.pub_protein_temp;

select * from scin_db.scin_pub_material_n_method;

SELECT * FROM scin_db.pub_technique_list;
SELECT * FROM scin_db.pub_protein_list;
SELECT * FROM scin_db.scin_pub_meta;

select count(1) from scin_db.scin_pub_meta;
select * from scin_db.scin_pub_meta;


-- select data from tables
select * from scin_pub_meta;
select * from scin_pub_material_n_method;
select * from scin_pub_result;
select * from scin_pub_figure;

# check no header 
select t1.id, t1.src_address from scin_pub_meta t1
  where not exists (
    select 1 from scin_pub_material_n_method t2
    where t1.id = t2.doc_id_id);

/* reset content */
/*
truncate scin_pub_material_n_method;
truncate scin_pub_figure;
truncate scin_pub_result;
delete from scin_pub_meta;
alter table scin_pub_material_n_method AUTO_INCREMENT = 1;
alter table scin_pub_result AUTO_INCREMENT = 1;
alter table scin_pub_figure AUTO_INCREMENT = 1;
alter table scin_pub_meta AUTO_INCREMENT = 1;
*/
/*
drop table scin_pub_material_n_method;
drop table scin_pub_figure;
drop table scin_pub_meta;
*/

alter table scin_pub_material_n_method modify header varchar(250);


select header, count(1) from scin_pub_material_n_method group by header order by count(1) desc;

select * from scin_pub_material_n_method;
select count(1) from scin_pub_meta;


SELECT table_schema "Data Base Name", SUM( data_length + index_length) / 1024 / 1024 
"Data Base Size in MB" FROM information_schema.TABLES GROUP BY table_schema ;


select count(1) from scin_db.scin_pub_result;





select count(distinct tr.doc_id)
from scin_db.pub_technique_result tr
inner join scin_db.pub_supplier_result sr
on tr.doc_id = sr.doc_id;
