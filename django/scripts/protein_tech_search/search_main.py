import sys
import MySQLdb
import codecs

import run_technique
import run_protein
import run_protein_tech
import flush_temp_tables

from warnings import filterwarnings

sys.setrecursionlimit(20000)
filterwarnings('ignore', category = MySQLdb.Warning)
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
try:
	mysql = MySQLdb.connect(user='root',passwd='password1',db='scin_db',host='127.0.0.1',port=3306, autocommit = 'True', charset = 'utf8', use_unicode = True)
	mysql_cursor = mysql.cursor()
	
	mysql_cursor.execute("SELECT id FROM scin_db.scin_pub_meta ht "
							"WHERE EXISTS ( "
							"SELECT 1 FROM scin_db.scin_pub_figure ft "
							"WHERE ht.id = ft.doc_id_id "
							") "
							"AND EXISTS ( "
							"SELECT 1 FROM scin_db.scin_pub_material_n_method mt "
							"WHERE mt.id = mt.doc_id_id "
							") "
							"AND id BETWEEN 17501 and 20000 "
							"ORDER BY id")
	
	for (id) in mysql_cursor:
	  doc_id = id
	  print "procesing doc_id: %d" % doc_id
	  techResult = run_technique.search_tech(doc_id)
	  if techResult > 0:
		protResult = run_protein.search_protein(doc_id)
		if protResult > 0:
			run_protein_tech.search_protein_tech(doc_id)
	  flush_temp_tables.flush_temp_tables(doc_id)
	  print "doc_id [%d] search completed" % doc_id
	
	mysql_cursor.close()
	mysql.close()

except MySQLdb.Error, e:
	errmsg = "MySQL Error (@%d) %d:  %s" % ( doc_id, e.args[0], e.args[1] )
	with open("error.log", 'w') as w:
		w.write(errmsg)
	sys.exit(1)