-- procedure 1a, scan and keep technique name exists in document
DROP PROCEDURE scin_db.pub_technique_exists;
CREATE PROCEDURE scin_db.pub_technique_exists(IN p_doc_id INT(11))
BEGIN

DECLARE v_tech_id INT(11);
DECLARE v_parental_name VARCHAR(100);
DECLARE v_alternative_name VARCHAR(100);
DECLARE done BOOLEAN DEFAULT FALSE;
DECLARE cur1 CURSOR FOR SELECT id, parental_name, alternative FROM scin_db.pub_technique_list;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

OPEN cur1;
techLoop: LOOP
    FETCH cur1 INTO v_tech_id, v_parental_name, v_alternative_name;
    IF done = TRUE THEN 
        CLOSE cur1;
        LEAVE techLoop;
    END IF;
    
    -- TOOD: use regex to search whole words instead, like is not appropriate
    IF EXISTS(SELECT 1
                FROM scin_db.scin_pub_material_n_method
                WHERE doc_id = p_doc_id
                AND (content LIKE concat('%', v_alternative_name,  '%') OR
                    header LIKE concat('%', v_alternative_name,  '%')
                    )
                ) THEN
        INSERT INTO scin_db.pub_technique_result (doc_id, tech_id, tech_parental_name, tech_alternative) 
            SELECT p_doc_id, id, parental_name, alternative
            FROM scin_db.pub_technique_list T1
            WHERE parental_name = v_parental_name
            AND NOT EXISTS (
              SELECT 1 FROM scin_db.pub_technique_result T2
              WHERE T2.doc_id = p_doc_id
              AND T2.tech_id = T1.id
            );
    END IF;
    
END LOOP techLoop;
END;


DROP PROCEDURE scin_db.pub_supplier_exists_by_sup;
CREATE PROCEDURE scin_db.pub_supplier_exists_by_sup(IN p_doc_id INT(11), IN p_supplier_id INT(11))
BEGIN

DECLARE v_supplier_id INT(11);
DECLARE v_supplier VARCHAR(100);
DECLARE done BOOLEAN DEFAULT FALSE;
DECLARE cur1 CURSOR FOR SELECT id, supplier FROM scin_db.pub_supplier_list WHERE id = p_supplier_id;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

OPEN cur1;
sppLoop: LOOP
    FETCH cur1 INTO v_supplier_id, v_supplier;
    IF done = TRUE THEN 
        CLOSE cur1;
        LEAVE sppLoop;
    END IF;
    
    -- TOOD: use regex to search whole words instead, like is not appropriate
    IF EXISTS(SELECT 1
                FROM scin_db.scin_pub_material_n_method
                WHERE doc_id = p_doc_id
                AND content LIKE concat('%', v_supplier,  '%')) THEN
        INSERT INTO scin_db.pub_supplier_result (doc_id, supplier_id, supplier) 
            SELECT p_doc_id, id, supplier
            FROM scin_db.pub_supplier_list T1
            WHERE id = v_supplier_id
            AND NOT EXISTS (
              SELECT 1 FROM scin_db.pub_supplier_result T2
              WHERE T2.doc_id = p_doc_id
              AND T2.supplier_id = T1.id
            );
    END IF;
    
END LOOP sppLoop;
END;


DROP PROCEDURE scin_db.pub_product_exists_by_sup;
CREATE PROCEDURE scin_db.pub_product_exists_by_sup(IN p_doc_id INT(11), IN p_supplier_id INT(11))
BEGIN

DECLARE v_prod_id INT(11);
DECLARE v_supplier VARCHAR(100);
DECLARE v_catalog_nb VARCHAR(100);
DECLARE done BOOLEAN DEFAULT FALSE;
DECLARE cur1 CURSOR FOR
  SELECT lt.id, lt.supplier, lt.catalog_nb 
  FROM scin_db.pub_product_info lt
  INNER JOIN scin_db.pub_supplier_result rt
  ON rt.supplier_id = lt.supplier_id
  WHERE doc_id = p_doc_id
  AND lt.supplier_id = p_supplier_id;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

OPEN cur1;
catLoop: LOOP
    FETCH cur1 INTO v_prod_id, v_supplier, v_catalog_nb;
    IF done = TRUE THEN 
        CLOSE cur1;
        LEAVE catLoop;
    END IF;
    
    -- TOOD: use regex to search whole words instead, like is not appropriate
    IF EXISTS(SELECT 1
                FROM scin_db.scin_pub_material_n_method
                WHERE doc_id = p_doc_id
                AND content LIKE concat('%', v_catalog_nb,  '%')) THEN
        INSERT INTO scin_db.pub_product_result (doc_id, prod_id, supplier, catalog_nb) 
            SELECT p_doc_id, id, supplier, catalog_nb
            FROM scin_db.pub_product_info T1
            WHERE id = v_prod_id
            AND NOT EXISTS (
              SELECT 1 FROM scin_db.pub_product_result T2
              WHERE T2.doc_id = p_doc_id
              AND T2.prod_id = T1.id
            );
    END IF;
    
END LOOP catLoop;
END;

DROP PROCEDURE scin_db.pub_technique_product_exists_by_sup;
CREATE PROCEDURE scin_db.pub_technique_product_exists_by_sup(IN p_doc_id INT(11), IN p_supplier_id INT(11))
BEGIN

DECLARE v_tech_id INT(11);
DECLARE v_parental_name VARCHAR(100);
DECLARE v_alternative VARCHAR(100);
DECLARE v_prod_id INT(11);
DECLARE v_supplier_name VARCHAR(100);
DECLARE v_catalog_nb VARCHAR(100);
DECLARE v_prod_name1 VARCHAR(40);
DECLARE v_prod_name2 VARCHAR(40);
DECLARE v_prod_name3 VARCHAR(40);
DECLARE v_prod_name4 VARCHAR(40);
DECLARE v_prod_name5 VARCHAR(40);
DECLARE v_figure_id INT(11);
DECLARE v_doc_figure_id INT(11);
DECLARE v_content LONGTEXT;
DECLARE cur1_done BOOLEAN DEFAULT FALSE;
DECLARE cur2_done BOOLEAN DEFAULT FALSE;
DECLARE cur3_done BOOLEAN DEFAULT FALSE;

DECLARE cur1 CURSOR FOR 
    SELECT tech_id, tech_parental_name, tech_alternative FROM scin_db.pub_technique_result WHERE doc_id = p_doc_id;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET cur1_done = TRUE;

OPEN cur1;
cur1_loop: LOOP
FETCH FROM cur1 INTO v_tech_id, v_parental_name, v_alternative;
    
    IF cur1_done then
        CLOSE cur1;
        LEAVE cur1_loop;
    END IF;
    BLOCK2: BEGIN
    DECLARE cur2 CURSOR FOR 
        SELECT DISTINCT pr_tab.prod_id, pi_tab.supplier, pi_tab.catalog_nb, pn_tab.name1, pn_tab.name2, pn_tab.name3, pn_tab.name4, pn_tab.name5 
        FROM scin_db.pub_product_info pi_tab
        INNER JOIN scin_db.pub_product_name pn_tab
        ON pi_tab.id = pn_tab.id
        INNER JOIN scin_db.pub_product_result pr_tab
        ON pn_tab.id = pr_tab.prod_id
        WHERE pr_tab.doc_id = p_doc_id
		    AND pi_tab.supplier_id = p_supplier_id;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET cur2_done = TRUE;
    
    OPEN cur2;
    cur2_loop: LOOP
    FETCH FROM cur2 INTO v_prod_id, v_supplier_name, v_catalog_nb, v_prod_name1, v_prod_name2, v_prod_name3, v_prod_name4, v_prod_name5;
    
      IF cur2_done then
        SET cur1_done = FALSE;
        CLOSE cur2;
        LEAVE cur2_loop;
      END IF;
      
      BLOCK3: BEGIN
      DECLARE cur3 CURSOR FOR SELECT id, figure_id FROM scin_db.scin_pub_figure WHERE doc_id = p_doc_id;
      DECLARE CONTINUE HANDLER FOR NOT FOUND SET cur3_done = TRUE;
      
      OPEN cur3;
      cur3_loop: LOOP
      FETCH FROM cur3 INTO v_figure_id, v_doc_figure_id;
      
        IF cur3_done then
          SET cur1_done = FALSE;
          SET cur2_done = FALSE;
          CLOSE cur3;
          LEAVE cur3_loop;
        END IF;
      
        -- CHECK technique presence and insert all keywords
        IF EXISTS (SELECT 1
                  FROM scin_db.scin_pub_figure
                  WHERE id = v_figure_id
                  AND CONTENT LIKE concat('%', v_alternative,  '%')) THEN
          
          IF v_prod_name1 IS NOT NULL THEN
           INSERT INTO scin_db.pub_tech_prod_temp (doc_id, figure_id, tech_id, tech_parental_name, tech_alternative, prod_id, supplier, catalog_nb, product_name, content)
             SELECT doc_id, v_figure_id, v_tech_id, v_parental_name, v_alternative, v_prod_id, v_supplier_name, v_catalog_nb, v_prod_name1, content
             FROM scin_db.scin_pub_figure
             WHERE id = v_figure_id
             ;
          END IF;
                      
          IF v_prod_name2 IS NOT NULL THEN
           INSERT INTO scin_db.pub_tech_prod_temp (doc_id, figure_id, tech_id, tech_parental_name, tech_alternative, prod_id, supplier, catalog_nb, product_name, content)
             SELECT doc_id, v_figure_id, v_tech_id, v_parental_name, v_alternative, v_prod_id, v_supplier_name, v_catalog_nb, v_prod_name2, content
             FROM scin_db.scin_pub_figure
             WHERE id = v_figure_id
             ;
          END IF;
          
          IF v_prod_name3 IS NOT NULL THEN
           INSERT INTO scin_db.pub_tech_prod_temp (doc_id, figure_id, tech_id, tech_parental_name, tech_alternative, prod_id, supplier, catalog_nb, product_name, content)
             SELECT doc_id, v_figure_id, v_tech_id, v_parental_name, v_alternative, v_prod_id, v_supplier_name, v_catalog_nb, v_prod_name3, content
             FROM scin_db.scin_pub_figure
             WHERE id = v_figure_id
             ;
          END IF;
          
          IF v_prod_name4 IS NOT NULL THEN
           INSERT INTO scin_db.pub_tech_prod_temp (doc_id, figure_id, tech_id, tech_parental_name, tech_alternative, prod_id, supplier, catalog_nb, product_name, content)
             SELECT doc_id, v_figure_id, v_tech_id, v_parental_name, v_alternative, v_prod_id, v_supplier_name, v_catalog_nb, v_prod_name4, content
             FROM scin_db.scin_pub_figure
             WHERE id = v_figure_id
             ;
          END IF;
          
          IF v_prod_name5 IS NOT NULL THEN
           INSERT INTO scin_db.pub_tech_prod_temp (doc_id, figure_id, tech_id, tech_parental_name, tech_alternative, prod_id, supplier, catalog_nb, product_name, content)
             SELECT doc_id, v_figure_id, v_tech_id, v_parental_name, v_alternative, v_prod_id, v_supplier_name, v_catalog_nb, v_prod_name5, content
             FROM scin_db.scin_pub_figure
             WHERE id = v_figure_id
             ;
          END IF;
        END IF;
        
        -- implement here supportive information check here
        /*
        IF EXISTS (SELECT 1
                  FROM scin_db.scin_pub_support_info
                  WHERE doc_id = p_doc_id
                  AND header = CONCAT('Figure S' ,v_figure_id ,'.')
                  AND (CONTENT REGEXP CONCAT('([^.?!]+([[:space:]]', v_alternative, '[[:space:]])+.*([[:space:]]', v_prod_name1, '[[:space:]])+[^.?!]+\.)')
                      OR CONTENT REGEXP CONCAT('([^.?!]+([[:space:]]', v_prod_name5, '[[:space:]])+.*([[:space:]]', v_alternative, '[[:space:]])+[^.?!]+\.)'))) THEN
                      
           INSERT INTO scin_db.pub_tech_prod_temp (doc_id, figure_id, si_id, tech_id, tech_parental_name, tech_alternative, prod_id, supplier, catalog_nb, product_name, content)
             SELECT doc_id, figure_id, id, v_tech_id, v_parental_name, v_alternative, v_prod_id, v_supplier_name, v_catalog_nb, v_prod_name1, content
             FROM scin_db.scin_pub_support_info
             WHERE doc_id = p_doc_id
             AND header = CONCAT('Figure S' ,v_figure_id ,'.')
             ;
        END IF;
        IF EXISTS (SELECT 1
                  FROM scin_db.scin_pub_support_info
                  WHERE doc_id = p_doc_id
                  AND header = CONCAT('Figure S' ,v_figure_id ,'.')
                  AND (CONTENT REGEXP CONCAT('([^.?!]+([[:space:]]', v_alternative, '[[:space:]])+.*([[:space:]]', v_prod_name2, '[[:space:]])+[^.?!]+\.)')
                      OR CONTENT REGEXP CONCAT('([^.?!]+([[:space:]]', v_prod_name5, '[[:space:]])+.*([[:space:]]', v_alternative, '[[:space:]])+[^.?!]+\.)'))) THEN
                      
           INSERT INTO scin_db.pub_tech_prod_temp (doc_id, figure_id, si_id, tech_id, tech_parental_name, tech_alternative, prod_id, supplier, catalog_nb, product_name, content)
             SELECT doc_id, figure_id, id, v_tech_id, v_parental_name, v_alternative, v_prod_id, v_supplier_name, v_catalog_nb, v_prod_name2, content
             FROM scin_db.scin_pub_support_info
             WHERE doc_id = p_doc_id
             AND header = CONCAT('Figure S' ,v_figure_id ,'.')
             ;
        END IF;
        IF EXISTS (SELECT 1
                  FROM scin_db.scin_pub_support_info
                  WHERE doc_id = p_doc_id
                  AND header = CONCAT('Figure S' ,v_figure_id ,'.')
                  AND (CONTENT REGEXP CONCAT('([^.?!]+([[:space:]]', v_alternative, '[[:space:]])+.*([[:space:]]', v_prod_name1, '[[:space:]])+[^.?!]+\.)')
                      OR CONTENT REGEXP CONCAT('([^.?!]+([[:space:]]', v_prod_name5, '[[:space:]])+.*([[:space:]]', v_alternative, '[[:space:]])+[^.?!]+\.)'))) THEN
                      
           INSERT INTO scin_db.pub_tech_prod_temp (doc_id, figure_id, si_id, tech_id, tech_parental_name, tech_alternative, prod_id, supplier, catalog_nb, product_name, content)
             SELECT doc_id, figure_id, id, v_tech_id, v_parental_name, v_alternative, v_prod_id, v_supplier_name, v_catalog_nb, v_prod_name1, content
             FROM scin_db.scin_pub_support_info
             WHERE doc_id = p_doc_id
             AND header = CONCAT('Figure S' ,v_figure_id ,'.')
             ;
        END IF;
        IF EXISTS (SELECT 1
                  FROM scin_db.scin_pub_support_info
                  WHERE doc_id = p_doc_id
                  AND header = CONCAT('Figure S' ,v_figure_id ,'.')
                  AND (CONTENT REGEXP CONCAT('([^.?!]+([[:space:]]', v_alternative, '[[:space:]])+.*([[:space:]]', v_prod_name1, '[[:space:]])+[^.?!]+\.)')
                      OR CONTENT REGEXP CONCAT('([^.?!]+([[:space:]]', v_prod_name5, '[[:space:]])+.*([[:space:]]', v_alternative, '[[:space:]])+[^.?!]+\.)'))) THEN
                      
           INSERT INTO scin_db.pub_tech_prod_temp (doc_id, figure_id, si_id, tech_id, tech_parental_name, tech_alternative, prod_id, supplier, catalog_nb, product_name, content)
             SELECT doc_id, figure_id, id, v_tech_id, v_parental_name, v_alternative, v_prod_id, v_supplier_name, v_catalog_nb, v_prod_name1, content
             FROM scin_db.scin_pub_support_info
             WHERE doc_id = p_doc_id
             AND header = CONCAT('Figure S' ,v_figure_id ,'.')
             ;
        END IF;
        IF EXISTS (SELECT 1
                  FROM scin_db.scin_pub_support_info
                  WHERE doc_id = p_doc_id
                  AND header = CONCAT('Figure S' ,v_figure_id ,'.')
                  AND (CONTENT REGEXP CONCAT('([^.?!]+([[:space:]]', v_alternative, '[[:space:]])+.*([[:space:]]', v_prod_name1, '[[:space:]])+[^.?!]+\.)')
                      OR CONTENT REGEXP CONCAT('([^.?!]+([[:space:]]', v_prod_name5, '[[:space:]])+.*([[:space:]]', v_alternative, '[[:space:]])+[^.?!]+\.)'))) THEN
                      
           INSERT INTO scin_db.pub_tech_prod_temp (doc_id, figure_id, si_id, tech_id, tech_parental_name, tech_alternative, prod_id, supplier, catalog_nb, product_name, content)
             SELECT doc_id, figure_id, id, v_tech_id, v_parental_name, v_alternative, v_prod_id, v_supplier_name, v_catalog_nb, v_prod_name1, content
             FROM scin_db.scin_pub_support_info
             WHERE doc_id = p_doc_id
             AND header = CONCAT('Figure S' ,v_figure_id ,'.')
             ;
        END IF;
        */
      
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
  DELETE FROM scin_db.pub_tech_prod_temp;
END;

DROP PROCEDURE scin_db.pub_rerun_by_id;
CREATE PROCEDURE scin_db.pub_rerun_by_id(IN p_doc_id INT(11))
BEGIN
  DELETE FROM pub_product_result WHERE doc_id = p_doc_id;
  DELETE FROM pub_supplier_result WHERE doc_id = p_doc_id;
  DELETE FROM pub_technique_result WHERE doc_id = p_doc_id;
  DELETE FROM pub_tech_prod_result WHERE doc_id = p_doc_id;
  
  CALL scin_db.pub_technique_exists(p_doc_id);
  CALL scin_db.pub_supplier_exists(p_doc_id);
  CALL scin_db.pub_product_exists(p_doc_id);
  CALL scin_db.pub_technique_product_exists(p_doc_id);
END;