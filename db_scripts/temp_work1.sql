/*
create table pub_technique_result_20150510
  select * from pub_technique_result;
create table pub_supplier_result_20150510
  select * from pub_supplier_result;
create table pub_product_result_20150510
  select * from pub_product_result;
create table pub_tech_prod_result_20150510
  select * from pub_tech_prod_result;
  
  
truncate table pub_tech_prod_result;
truncate table pub_tech_prod_temp;
truncate table pub_product_result;
truncate table pub_supplier_result;
truncate table pub_technique_result;
*/

select * from pub_technique_result;
select * from pub_supplier_result;
select * from pub_product_result;
select * from pub_tech_prod_temp;
select * from pub_tech_prod_result;

call scin_db.pub_technique_exists(34710);
call scin_db.pub_supplier_exists(34710);
call scin_db.pub_product_exists(34710);
call scin_db.pub_technique_product_exists(34710);




SELECT *
FROM scin_db.scin_pub_meta
WHERE id = 34122;

SELECT *
FROM scin_db.scin_pub_figure
WHERE doc_id = 34710;

SELECT *
FROM scin_db.scin_pub_material_n_method
WHERE doc_id = 32576
AND (content LIKE concat('%', v_alternative_name,  '%') OR
    header LIKE concat('%', v_alternative_name,  '%')