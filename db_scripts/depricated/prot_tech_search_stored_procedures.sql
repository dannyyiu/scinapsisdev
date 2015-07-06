-- procedure 1a, scan and keep technique name exists in document
DROP PROCEDURE scin_db.pub_technique_exists;
CREATE PROCEDURE scin_db.pub_technique_exists(IN p_doc_id INT(11))
BEGIN

DECLARE v_parental_name VARCHAR(100);
DECLARE v_alternative_name VARCHAR(100);
DECLARE done BOOLEAN DEFAULT FALSE;
DECLARE cur1 CURSOR FOR SELECT parental_name, alternative FROM scin_db.pub_technique_list;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

OPEN cur1;
techLoop: LOOP
    FETCH cur1 INTO v_parental_name, v_alternative_name;
    IF done = TRUE THEN 
        CLOSE cur1;
        LEAVE techLoop;
    END IF;
    
    -- TOOD: use regex to search whole words instead, like is not appropriate
    IF EXISTS(SELECT 1
                FROM scin_db.scin_pub_material_n_method
                WHERE doc_id_id = p_doc_id
                AND content LIKE BINARY concat('%', v_alternative_name,  '%')) THEN
        INSERT INTO scin_db.pub_technique_temp (doc_id, tech_parental_name, tech_alternative) 
            SELECT p_doc_id, parental_name, alternative
            FROM scin_db.pub_technique_list T1
            WHERE parental_name = v_parental_name
            AND NOT EXISTS (
              SELECT 1 FROM scin_db.pub_technique_temp T2
              WHERE T2.doc_id = p_doc_id
              AND T2.tech_alternative = T1.alternative
            );
    END IF;
    
END LOOP techLoop;
END;

-- procedure 1b, scan and keep protein name exists in document
DROP PROCEDURE scin_db.pub_protein_exists;
CREATE PROCEDURE scin_db.pub_protein_exists(IN p_doc_id INT(11))
BEGIN

DECLARE v_gene_name VARCHAR(100);
DECLARE done BOOLEAN DEFAULT FALSE;
DECLARE cur1 CURSOR FOR SELECT gene_name FROM scin_db.pub_protein_list;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

OPEN cur1;
protLoop: LOOP
    FETCH cur1 INTO v_gene_name;
    IF done = TRUE THEN 
        CLOSE cur1;
        LEAVE protLoop;
    END IF;
    
    -- TOOD: use regex to search whole words instead, like is not appropriate
    IF EXISTS(SELECT 1
                FROM scin_db.scin_pub_figure
                WHERE doc_id_id = p_doc_id
                AND content LIKE BINARY concat('%', v_gene_name,  '%')) THEN
        INSERT INTO scin_db.pub_protein_temp (doc_id, protein_gene_name) 
            SELECT p_doc_id, gene_name
            FROM scin_db.pub_protein_list T1
            WHERE gene_name = v_gene_name
            AND NOT EXISTS (
              SELECT 1 FROM scin_db.pub_protein_temp T2
              WHERE T2.doc_id = p_doc_id
              AND T2.protein_gene_name = T1.gene_name
            );
    END IF;
    
END LOOP protLoop;

END;

#procedure 2, scan and keep both protein and technique exists in document
# reference: http://stackoverflow.com/questions/9699896/nested-cursors-in-mysql
DROP PROCEDURE scin_db.pub_technique_protein_exists;
CREATE PROCEDURE scin_db.pub_technique_protein_exists(IN p_doc_id INT(11))
BEGIN

DECLARE v_gene_name VARCHAR(100);
DECLARE v_parental_name VARCHAR(100);
DECLARE v_alternative VARCHAR(100);
DECLARE v_figure_id INT(11);
DECLARE v_content LONGTEXT;
DECLARE cur1_done BOOLEAN DEFAULT FALSE;
DECLARE cur2_done BOOLEAN DEFAULT FALSE;
DECLARE cur3_done BOOLEAN DEFAULT FALSE;

DECLARE cur1 CURSOR FOR 
    SELECT tech_parental_name, tech_alternative FROM scin_db.pub_technique_temp WHERE doc_id = p_doc_id;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET cur1_done = TRUE;

OPEN cur1;
cur1_loop: LOOP
    
    FETCH FROM cur1 INTO v_parental_name, v_alternative;
    IF cur1_done then
        CLOSE cur1;
        LEAVE cur1_loop;
    END IF;
    
    BLOCK2: BEGIN
    DECLARE cur2 CURSOR FOR 
        SELECT DISTINCT protein_gene_name FROM scin_db.pub_protein_temp WHERE doc_id = p_doc_id;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET cur2_done = TRUE;
    
    OPEN cur2;
    cur2_loop: LOOP
    
      FETCH FROM cur2 INTO v_gene_name;
      IF cur2_done then
        SET cur1_done = FALSE;
        CLOSE cur2;
        LEAVE cur2_loop;
      END IF;
      
      BLOCK3: BEGIN
      DECLARE cur3 CURSOR FOR SELECT figure_id FROM scin_db.scin_pub_figure WHERE doc_id_id = p_doc_id;
      DECLARE CONTINUE HANDLER FOR NOT FOUND SET cur3_done = TRUE;
      
      OPEN cur3;
      cur3_loop: LOOP
      
        FETCH FROM cur3 INTO v_figure_id;
        IF cur3_done then
          SET cur1_done = FALSE;
          SET cur2_done = FALSE;
          CLOSE cur3;
          LEAVE cur3_loop;
        END IF;
      
        -- TODO: use REGEX instead
        IF EXISTS (SELECT 1
                  FROM scin_db.scin_pub_figure
                  WHERE doc_id_id = p_doc_id
                  AND figure_id = v_figure_id
                  AND (CONTENT REGEXP CONCAT('([^.?!]+([[:space:]]', v_alternative, '[[:space:]])+.*(([[:space:]]|-)', v_gene_name, '[[:space:]])+[^.?!]+\.)')
                      OR CONTENT REGEXP CONCAT('([^.?!]+(([[:space:]|-])', v_gene_name, '[[:space:]])+.*([[:space:]]', v_alternative, '[[:space:]])+[^.?!]+\.)'))) THEN
--                   AND (CONTENT LIKE BINARY concat('%', v_gene_name, '%', v_alternative, '%') OR
--                       CONTENT LIKE BINARY concat('%', v_alternative, '%', v_gene_name, '%'))) THEN
                      
           INSERT INTO scin_db.pub_tech_protein_temp
             SELECT doc_id_id, v_gene_name, v_parental_name, v_alternative, figure_id, content
             FROM scin_db.scin_pub_figure
             WHERE doc_id_id = p_doc_id
             AND figure_id = v_figure_id
             ;
        END IF;
      
      END LOOP cur3_loop;
      END BLOCK3;
      
      -- reset value
      SET cur3_done = FALSE;
    
    END LOOP cur2_loop;
    END BLOCK2;
    
    -- reset value
    SET cur2_done = FALSE;

END LOOP cur1_loop;

END;

DROP PROCEDURE scin_db.pub_flush_temp_tables;
CREATE PROCEDURE scin_db.pub_flush_temp_tables(IN p_doc_id INT(11))
BEGIN
  DELETE FROM scin_db.pub_technique_temp WHERE doc_id = p_doc_id;
  DELETE FROM scin_db.pub_protein_temp WHERE doc_id = p_doc_id;
  DELETE FROM scin_db.pub_tech_protein_temp  WHERE doc_id = p_doc_id;
END;