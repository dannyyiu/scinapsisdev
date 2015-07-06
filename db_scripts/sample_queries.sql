-- get search result per user input
select doc_id, pub_figure_id, tech_parental_name as technique, supplier_name, catalog_nb, sentence
from pub_tech_prod_result
where catalog_nb = 'NB100-139';

-- get figure information
select fig.*
from scin_pub_figure fig
inner join pub_tech_prod_result rslt
on fig.doc_id_id = rslt.doc_id
and fig.figure_id = rslt.pub_figure_id
where rslt.catalog_nb = 'NB100-139';

-- get publication information
select meta.*
from scin_pub_meta meta
inner join pub_tech_prod_result rslt
on meta.id = rslt.doc_id
where rslt.catalog_nb = 'NB100-139';
