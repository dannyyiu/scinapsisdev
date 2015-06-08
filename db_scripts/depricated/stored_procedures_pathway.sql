DROP PROCEDURE scin_db.pub_pw_action_word_exists;
CREATE PROCEDURE scin_db.pub_pw_action_word_exists(IN p_doc_id INT(11))
BEGIN

DECLARE v_phase VARCHAR(100);
DECLARE v_group_name VARCHAR(100);
DECLARE done BOOLEAN DEFAULT FALSE;
DECLARE cur1 CURSOR FOR SELECT phase, group_name FROM scin_db.pub_action_word_list;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

OPEN cur1;
actionLoop: LOOP
    FETCH cur1 INTO v_phase, v_group_name;
    IF done = TRUE THEN 
        CLOSE cur1;
        LEAVE actionLoop;
    END IF;
    
    -- TOOD: use regex to search whole words instead, like is not appropriate
    IF EXISTS(SELECT 1
                FROM scin_db.scin_pub_result
                WHERE doc_id_id = p_doc_id
                AND content LIKE BINARY concat('%', v_phase,  '%')) THEN
        INSERT INTO scin_db.pub_pw_action_word_temp (doc_id, phase, group_name) 
            SELECT p_doc_id, phase, group_name
            FROM scin_db.pub_action_word_list T1
            WHERE phase = v_phase
            AND NOT EXISTS (
              SELECT 1 FROM scin_db.pub_pw_action_word_temp T2
              WHERE T2.doc_id = p_doc_id
              AND T2.phase = T1.phase
            );
    END IF;
    
END LOOP actionLoop;
END;



DROP PROCEDURE scin_db.pub_pw_protein_exists;
CREATE PROCEDURE scin_db.pub_pw_protein_exists(IN p_doc_id INT(11))
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
                FROM scin_db.scin_pub_result
                WHERE doc_id_id = p_doc_id
                AND content LIKE BINARY concat('%', v_gene_name,  '%')) THEN
        INSERT INTO scin_db.pub_pw_protein_temp (doc_id, protein_gene_name) 
            SELECT p_doc_id, gene_name
            FROM scin_db.pub_protein_list T1
            WHERE gene_name = v_gene_name
            AND NOT EXISTS (
              SELECT 1 FROM scin_db.pub_pw_protein_temp T2
              WHERE T2.doc_id = p_doc_id
              AND T2.protein_gene_name = T1.gene_name
            );
    END IF;
    
END LOOP protLoop;

END;

DROP PROCEDURE scin_db.pub_pathway_exists;
CREATE PROCEDURE scin_db.pub_pathway_exists(IN p_doc_id INT(11))
BEGIN

DECLARE v_gene_name1 VARCHAR(100);
DECLARE v_gene_name2 VARCHAR(100);
DECLARE v_phase VARCHAR(20);
DECLARE v_phase_group_name VARCHAR(20);
DECLARE v_section_id INT(11);
DECLARE v_content_seq INT(11);
DECLARE v_content LONGTEXT;
DECLARE cur1_done BOOLEAN DEFAULT FALSE;
DECLARE cur2_done BOOLEAN DEFAULT FALSE;
DECLARE cur3_done BOOLEAN DEFAULT FALSE;

DECLARE cur1 CURSOR FOR 
    SELECT t1.protein_gene_name, t2.protein_gene_name 
    FROM scin_db.pub_pw_protein_temp AS t1
    LEFT JOIN scin_db.pub_pw_protein_temp AS t2
    ON t1.doc_id = t2.doc_id
    AND t1.protein_gene_name <> t2.protein_gene_name
    WHERE t1.doc_id = p_doc_id
    ORDER BY t1.protein_gene_name, t2.protein_gene_name;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET cur1_done = TRUE;

OPEN cur1;
cur1_loop: LOOP
    
    FETCH FROM cur1 INTO v_gene_name1, v_gene_name2;
    IF cur1_done then
        CLOSE cur1;
        LEAVE cur1_loop;
    END IF;
    
    BLOCK2: BEGIN
    DECLARE cur2 CURSOR FOR 
        SELECT DISTINCT phase, group_name FROM scin_db.pub_pw_action_word_temp WHERE doc_id = p_doc_id;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET cur2_done = TRUE;
    
    OPEN cur2;
    cur2_loop: LOOP
    
      FETCH FROM cur2 INTO v_phase, v_phase_group_name;
      IF cur2_done then
        SET cur1_done = FALSE;
        CLOSE cur2;
        LEAVE cur2_loop;
      END IF;
      
      BLOCK3: BEGIN
      DECLARE cur3 CURSOR FOR 
          SELECT section_id, content_seq FROM scin_db.scin_pub_result WHERE doc_id_id = p_doc_id;
      DECLARE CONTINUE HANDLER FOR NOT FOUND SET cur3_done = TRUE;
      
      OPEN cur3;
      cur3_loop: LOOP
      
        FETCH FROM cur3 INTO v_section_id, v_content_seq;
        IF cur3_done then
          SET cur1_done = FALSE;
          SET cur2_done = FALSE;
          CLOSE cur3;
          LEAVE cur3_loop;
        END IF;
      
        -- TODO: use REGEX instead
        IF EXISTS (SELECT 1
                  FROM scin_db.scin_pub_result
                  WHERE doc_id_id = p_doc_id
                  AND section_id = v_section_id
                  AND content_seq = v_content_seq
                  AND (CONTENT REGEXP CONCAT('([^.?!]+([[:space:]]', v_gene_name1, '[[:space:]])+.*([[:space:]]', v_phase, '[[:space:]])+.*([[:space:]]', v_gene_name2, '[[:space:]])+[^.?!]+\.)'))) THEN
                      
           INSERT INTO scin_db.pub_pathway_temp
             SELECT doc_id_id, v_gene_name1, v_gene_name2, v_phase, v_phase_group_name, v_section_id, v_content_seq, content
             FROM scin_db.scin_pub_result
             WHERE doc_id_id = p_doc_id
             AND section_id = v_section_id
             AND content_seq = v_content_seq
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


DROP PROCEDURE scin_db.pub_flush_pw_temp_tables;
CREATE PROCEDURE scin_db.pub_flush_pw_temp_tables(IN p_doc_id INT(11))
BEGIN
  DELETE FROM scin_db.pub_pw_action_word_temp WHERE doc_id = p_doc_id;
  DELETE FROM scin_db.pub_pw_protein_temp WHERE doc_id = p_doc_id;
  DELETE FROM scin_db.pub_pathway_temp  WHERE doc_id = p_doc_id;
END;


DROP TABLE scin_db.pub_pw_action_word_temp;
CREATE TABLE scin_db.pub_pw_action_word_temp (
    doc_id              INT(11),
    phase               VARCHAR(100),
    group_name          VARCHAR(100)
);

DROP TABLE scin_db.pub_pw_protein_temp;
CREATE TABLE scin_db.pub_pw_protein_temp (
    doc_id              INT(11),
    protein_gene_name   VARCHAR(100)
);

DROP TABLE scin_db.pub_pathway_temp;
CREATE TABLE scin_db.pub_pathway_temp (
    doc_id              INT(11),
    protein_gene_name1  VARCHAR(100),
    protein_gene_name2  VARCHAR(100),
    phase               VARCHAR(20),
    phase_group_name    VARCHAR(20),
    section_id          INT(11),
    content_seq         INT(11),
    content             LONGTEXT
);

DROP TABLE scin_db.pub_pathway_result;
CREATE TABLE scin_db.pub_pathway_result (
    doc_id              INT(11),
    protein_gene_name1  VARCHAR(100),
    protein_gene_name2  VARCHAR(100),
    phase               VARCHAR(20),
    phase_group_name    VARCHAR(20),
    section_id          INT(11),
    content_seq         INT(11),
    sentence            LONGTEXT
);

