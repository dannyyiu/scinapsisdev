/* PART I. remove composite keys from product tables
  1. add id for product tables
  2. change to use id in result table
  3. add product key
*/

-- backup original tables
create table pub_product_info_bk as select * from pub_product_info;
create table pub_product_name_bk as select * from pub_product_name;
create table pub_product_result_bk as select * from pub_prod_result;

-- insert record back into original table
-- COMMENT: uncertain in row order from _bk table, this would make row_number problem
-- another option is rebuild those tables from excel
insert into pub_product_info (supplier, catalog_nb, product_desc, url, application, host, immunogen, reactivity_human, reactivity_mouse)
select supplier, catalog_nb, product_desc, url, application, host, immunogen, reactivity_human, reactivity_mouse from pub_product_info_bk;

insert into pub_product_name (id, name1, name2, name3, name4, name5)
select info.id, name.name1, name.name2, name.name3, name.name4, name.name5
from pub_product_info info
inner join pub_product_name_bk name
on info.supplier = name.supplier
and info.catalog_nb = name.catalog_nb;

insert into pub_product_result (doc_id, prod_id, supplier, catalog_nb)
select rslt.doc_id, info.id, rslt.supplier_name, rslt.catalog_nb
from pub_product_result_bk rslt
inner join pub_product_info info
on rslt.supplier_name = info.supplier
and rslt.catalog_nb = info.catalog_nb;

/* part II. remove composite keys from technique list
  1. backup table
  2. apply new schemas
  3. restore table
*/
-- create backup tables
create table pub_technique_list_bk as select * from pub_technique_list;
create table pub_technique_result_bk as select * from pub_technique_result;

-- restore data back into technique list
-- COMMENT: uncertain in row order from _bk table, this would make row_number problem
-- another option is rebuild those tables from excel
insert into pub_technique_list (parental_name, alternative)
  select parental_name, alternative from pub_technique_list_bk;
insert into pub_technique_result (doc_id, tech_id, tech_parental_name, tech_alternative)
  select rslt.doc_id, list.id, rslt.tech_parental_name, rslt.tech_alternative
  from pub_technique_result_bk rslt
  inner join pub_technique_list list
  on rslt.tech_parental_name = list.parental_name
  and rslt.tech_alternative = list.alternative;
  
 
/* PART III.  change pub_supplier_list
  1. backup table
  2. apply new schemas
  3. restore table
*/
create table pub_supplier_result_bk
  as select * from pub_supplier_result;
  
insert into pub_supplier_result (supplier)
  select supplier_name from pub_supplier_result_bk;

  
/* PART IV.  change tech_prod result table to use id from figrure, product and technique
  1. backup table
  2. apply new schemas
  3. restore table
*/
create table pub_tech_prod_result_bk
  as select * from pub_tech_prod_result;

-- restore data back into technqiue list
insert into pub_tech_prod_result (doc_id, figure_id, tech_id, tech_parental_name, tech_alternative, prod_id, supplier, catalog_nb, product_name, sentence)
  select rslt.doc_id, fig.id, list.id, rslt.tech_parental_name, rslt.tech_alternative, info.id, rslt.supplier_name, rslt.catalog_nb, rslt.product_name, rslt.sentence
  from pub_tech_prod_result_bk rslt
  inner join scin_pub_figure fig
  on rslt.doc_id = fig.doc_id_id
  and rslt.figure_id = fig.figure_id
  inner join pub_technique_list list
  on rslt.tech_parental_name = list.parental_name
  and rslt.tech_alternative = list.alternative
  inner join pub_product_info info
  on rslt.supplier_name = info.supplier
  and rslt.catalog_nb = info.catalog_nb;