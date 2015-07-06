select * from scin_db.scin_pub_meta where id = 6;
select max(id) from scin_db.scin_pub_meta;

-- SIMLATION: STEP 1a - search if protein exists
call scin_db.pub_pw_action_word_exists(6);
select * from scin_db.pub_pw_action_word_temp;

-- SIMLATION: STEP 1b - search if protein exists
call scin_db.pub_pw_protein_exists(6);
select * from scin_db.pub_pw_protein_temp;

-- SIMLATION: STEP 1c - search if protein exists
-- drop table scin_db.log_tab;
-- create table scin_db.log_tab
-- (
--   log varchar(500)
-- );
call scin_db.pub_pathway_exists(5);
select * from scin_db.pub_pathway_temp;
select * from scin_db.pub_pathway_result;

-- 1 to 6
SELECT *
FROM scin_db.scin_pub_result
WHERE doc_id_id = 6
AND section_id = 1
AND content_seq = 1
AND (CONTENT REGEXP CONCAT('([^.?!]+([[:space:]]', 'SP+', '[[:space:]])+.*([[:space:]]', 'increase', '[[:space:]])+.*([[:space:]]', 'ALDH', '[[:space:]])+[^.?!]+\.)'))



-- SIMULATION: STEP 1d - flush tables
call scin_db.pub_flush_pw_temp_tables(50);

-- 72
SELECT t1.protein_gene_name, t2.protein_gene_name 
FROM scin_db.pub_pw_protein_temp AS t1
LEFT JOIN scin_db.pub_pw_protein_temp AS t2
ON t1.doc_id = t2.doc_id
AND t1.protein_gene_name <> t2.protein_gene_name
WHERE t1.doc_id = 1
ORDER BY t1.protein_gene_name, t2.protein_gene_name;

-- 19
SELECT DISTINCT phase, group_name FROM scin_db.pub_action_word_list;

-- 9
SELECT section_id, content_seq FROM scin_db.scin_pub_result WHERE doc_id_id = 1;


