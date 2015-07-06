DROP PROCEDURE scin_db.figure_tech_exists;
CREATE PROCEDURE scin_db.figure_tech_exists()
BEGIN

DECLARE v_figure_id INT(11);
DECLARE v_tech_id INT(11);
DECLARE v_technique_group VARCHAR(100);
DECLARE v_parental_name VARCHAR(100);
DECLARE v_alternative VARCHAR(100);

DECLARE cur1_done BOOLEAN DEFAULT FALSE;
DECLARE cur2_done BOOLEAN DEFAULT FALSE;

DECLARE cur1 CURSOR FOR 
    SELECT id FROM scin_db.scin_pub_figure ORDER BY id;
DECLARE CONTINUE HANDLER FOR NOT FOUND SET cur1_done = TRUE;

OPEN cur1;
cur1_loop: LOOP
FETCH FROM cur1 INTO v_figure_id;
    
    IF cur1_done then
        CLOSE cur1;
        LEAVE cur1_loop;
    END IF;
    
    BLOCK2: BEGIN
    DECLARE cur2 CURSOR FOR 
        SELECT id, technique_group, parental_name, alternative FROM scin_db.pub_technique_list;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET cur2_done = TRUE;
    
    OPEN cur2;
    cur2_loop: LOOP
    FETCH FROM cur2 INTO v_tech_id, v_technique_group, v_parental_name, v_alternative;
    
      IF cur2_done then
        SET cur1_done = FALSE;
        CLOSE cur2;
        LEAVE cur2_loop;
      END IF;
      
      -- CHECK technique presence and insert all keywords
      IF EXISTS (SELECT 1
                FROM scin_db.scin_pub_figure
                WHERE id = v_figure_id
                AND CONTENT LIKE concat('%', v_alternative,  '%')) THEN
        
         INSERT INTO scin_db.figure_tech (figure_id, tech_id, technique_group, tech_parental_name, tech_alternative, doc_id, header, content)
           SELECT id, v_tech_id, v_technique_group, v_parental_name, v_alternative, doc_id, header, content
           FROM scin_db.scin_pub_figure
           WHERE id = v_figure_id
           ;
          
        COMMIT;
        
      END IF;
    
    END LOOP cur2_loop;
    END BLOCK2;
    
    -- reset value
    SET cur2_done = FALSE;

END LOOP cur1_loop;

END;